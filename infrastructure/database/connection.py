import sqlite3
from contextlib import contextmanager

DB_NAME = "database.db"


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    
    try:
        yield conn
    finally:
        conn.close()