from interfaces.cli.main import main as cli_main

from infrastructure.database.connection import get_connection

def init_db():
    with open("infrastructure/database/schema.sql") as f:
        sql = f.read()

    with get_connection() as conn:
        conn.executescript(sql)
        conn.commit()

if __name__ == "__main__":
    init_db()
    cli_main()
