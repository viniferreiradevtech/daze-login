import os
from contextlib import closing
from datetime import timedelta
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import check_password_hash, generate_password_hash

from database import get_connection, init_db

load_dotenv()

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ["SECRET_KEY"],            # assina o cookie de sessão
    SESSION_COOKIE_HTTPONLY=True,                   # JS não consegue ler o cookie
    SESSION_COOKIE_SAMESITE="Lax",                  # reduz risco de CSRF
    SESSION_COOKIE_SECURE=os.getenv("FLASK_ENV") == "production",  # só HTTPS em produção
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),   # duração quando "lembrar" está marcado
)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per hour"],
    storage_uri="memory://",
)

# Hash falso usado quando o usuário não existe (explicação mais abaixo)
HASH_FALSO = generate_password_hash("senha-falsa-para-igualar-tempo")

init_db()


# ---------- Proteção de rotas ----------
def login_required(funcao):
    @wraps(funcao)
    def protegida(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("index"))
        return funcao(*args, **kwargs)
    return protegida


# ---------- Páginas ----------
@app.get("/")
def index():
    if "user_id" in session:
        return redirect(url_for("painel"))
    return render_template("index.html")


@app.get("/painel")
@login_required
def painel():
    return render_template("painel.html", usuario=session["usuario"])


# ---------- API ----------
@app.post("/api/login")
@limiter.limit("5 per minute")
def api_login():
    dados = request.get_json(silent=True) or {}
    usuario = dados.get("usuario")
    senha = dados.get("senha")
    lembrar = bool(dados.get("lembrar"))

    if (
        not isinstance(usuario, str)
        or not isinstance(senha, str)
        or not usuario.strip()
        or not senha
    ):
        return jsonify(erro="Informe usuário e senha."), 400

    # "?" = consulta parametrizada: impede SQL Injection
    with closing(get_connection()) as conn:
        linha = conn.execute(
            "SELECT id, usuario, senha_hash FROM usuarios WHERE usuario = ?",
            (usuario.strip(),),
        ).fetchone()

    # Sempre confere um hash, mesmo se o usuário não existir,
    # para que o tempo de resposta não revele quais usuários existem.
    hash_para_checar = linha["senha_hash"] if linha else HASH_FALSO
    senha_correta = check_password_hash(hash_para_checar, senha)

    if linha is None or not senha_correta:
        app.logger.warning("Falha de login para '%s' (IP %s)", usuario.strip(), request.remote_addr)
        # Mensagem genérica de propósito: não diz se foi o usuário ou a senha
        return jsonify(erro="Usuário ou senha inválidos."), 401

    session.clear()  # descarta qualquer sessão antiga (evita session fixation)
    session["user_id"] = linha["id"]
    session["usuario"] = linha["usuario"]
    session.permanent = lembrar

    return jsonify(ok=True, redirecionar=url_for("painel"))


@app.post("/api/logout")
def api_logout():
    session.clear()
    return jsonify(ok=True)


@app.errorhandler(429)
def muitas_tentativas(_erro):
    return jsonify(erro="Muitas tentativas. Aguarde um minuto e tente de novo."), 429


if __name__ == "__main__":
    app.run(debug=True)  # debug só em desenvolvimento!