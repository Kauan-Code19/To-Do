from app.interfaces.log_repository import LogRepository
from domain.entities.log import Log
from infrastructure.database.connection import get_connection

class SQLiteLogRepository(LogRepository):

    def create(self, log: Log) -> Log:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO logs (task_id, action, date)
                VALUES (?, ?, ?)
                """,
                (log.task_id, log.action, log.date),
            )

            log.id = cursor.lastrowid
            conn.commit()

        return log
    
    def get_all(self) -> list[Log]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, task_id, action, date FROM logs")
            rows = cursor.fetchall()

        logs = []
        for row in rows:
            log = Log(
                task_id=row["task_id"],
                action=row["action"],
            )
            log.id = row["id"]
            log.date = row["date"]
            logs.append(log)

        return logs