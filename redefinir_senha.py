from contextlib import closing
from getpass import getpass

from werkzeug.security import generate_password_hash

from database import get_connection, init_db


def main():
    init_db()

    usuario = input("Usuário: ").strip()
    senha = getpass("Nova senha: ")
    confirmacao = getpass("Repita a nova senha: ")

    if senha != confirmacao:
        print("As senhas não conferem. Nada foi alterado.")
        return
    if len(senha) < 6:
        print("A senha deve ter pelo menos 6 caracteres.")
        return

    with closing(get_connection()) as conn, conn:
        cursor = conn.execute(
            "UPDATE usuarios SET senha_hash = ? WHERE usuario = ?",
            (generate_password_hash(senha), usuario),
        )

    if cursor.rowcount == 0:
        print("Usuário não encontrado.")
    else:
        print(f"Senha de '{usuario}' atualizada com sucesso!")


if __name__ == "__main__":
    main()