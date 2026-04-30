
from app.interfaces.task_repository import TaskRepository
from domain.entities.task import Task
from domain.enums.task_status import TaskStatus
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
    
    def get_all(self) -> list[Task]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()

            tasks = []
            for row in rows:
                task = Task(
                    title=row["title"],
                    priority=row["priority"],
                    description=row["description"],
                    status=TaskStatus(row["status"]),
                )

                task.id = row["id"]
                task.created_date = row["creation_date"]
                task.deadline = row["deadline"]
                task.completion_date = row["completion_date"]

                tasks.append(task)

        return tasks