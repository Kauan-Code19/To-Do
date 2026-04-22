
from app.interfaces.task_repository import TaskRepository
from domain.entities.task import Task
from infrastructure.database.connection import get_connection


class SQLiteTaskRepository(TaskRepository):
    def create(self, task: Task) -> Task:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO tasks (title, description, priority, status, creation_date, deadline, completion_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task.title,
                    task.description,
                    task.priority,
                    task.status.value,
                    task.creation_date,
                    task.deadline,
                    task.completion_date,
                ),
            )

            task.id = cursor.lastrowid
            conn.commit()

        return task