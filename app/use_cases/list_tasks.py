from domain.entities.task import Task
from app.interfaces.task_repository import TaskRepository


class ListTasks:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self) -> list[Task]:
        return self.task_repository.get_all()