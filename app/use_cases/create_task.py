from app.interfaces.task_repository import TaskRepository
from domain.entities.task import Task


class CreateTask:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, title: str, priority: int, description: str = None) -> Task:
        task = Task(
            title=title,
            priority=priority,
            description=description,
        )

        return self.task_repository.create(task)