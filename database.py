import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).parent / "daze.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acessar colunas por nome: linha["usuario"]
    return conn


def init_db():
    """Cria a tabela de usuários caso ainda não exista."""
    with closing(get_connection()) as conn, conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario    TEXT NOT NULL UNIQUE COLLATE NOCASE,
                senha_hash TEXT NOT NULL,
                criado_em  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        