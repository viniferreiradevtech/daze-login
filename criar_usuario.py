import re
import sqlite3
from contextlib import closing
from getpass import getpass

from werkzeug.security import generate_password_hash

from database import get_connection, init_db

REGEX_USUARIO = re.compile(r"^[\w.\-]{3,30}$")


def main():
    init_db()

    usuario = input("Usuário: ").strip()
    if not REGEX_USUARIO.match(usuario):
        print("Usuário inválido: use de 3 a 30 letras, números, ponto, hífen ou underline.")
        return

    senha = getpass("Senha (não aparece enquanto digita): ")
    if len(senha) < 6:
        print("A senha deve ter pelo menos 6 caracteres.")
        return

    try:
        with closing(get_connection()) as conn, conn:
            conn.execute(
                "INSERT INTO usuarios (usuario, senha_hash) VALUES (?, ?)",
                (usuario, generate_password_hash(senha)),
            )
        print(f"Usuário '{usuario}' criado com sucesso!")
    except sqlite3.IntegrityError:
        print("Esse usuário já existe.")


if __name__ == "__main__":
    main()