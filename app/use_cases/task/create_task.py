from app.interfaces.task_repository import TaskRepository
from domain.entities.task import Task
from domain.entities.log import Log
from app.container import container

class CreateTask:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, title: str, priority: int, description: str = None):
        task = Task(
            title=title,
            priority=priority,
            description=description,
        )

        task = self.task_repository.create(task)
        container.log_service.create_log(task_id=task.id, action="created")
    
        return task