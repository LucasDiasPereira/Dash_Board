import sqlite3
from contextlib import contextmanager


@contextmanager
def connect():
    connect: sqlite3.Connection = sqlite3.connect('tabelas.db')
    try:
        yield connect
    finally:
        connect.close()


with connect() as conn:
    conn.execute(
        """--sql
        CREATE TABLE IF NOT EXISTS receita (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movimentacao TEXT NOT NULL,
            origem TEXT NOT NULL,
            categoria TEXT NOT NULL,
            data_hora TEXT NOT NULL,
            valor REAL NOT NULL
        );
        """
    )
