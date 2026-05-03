from app.container import container
from app.interfaces.task_repository import TaskRepository
from domain.entities.task import Task
from domain.enums.task_status import TaskStatus


class UpdateTask:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
        
    def execute(
        self,
        task_id: int,
        title: str = None,
        priority: int = None,
        description: str = None,
        status: TaskStatus = None
    ) -> Task:

        task = self._get_valid_task(task_id)

        other_changes, status_changed = self._apply_updates(
            task,
            title=title,
            priority=priority,
            description=description,
            status=status
        )

        task = self.task_repository.update(task)

        self._log_changes(task.id, other_changes, status_changed)

        return task
    
    def _get_valid_task(self, task_id: int) -> Task:
        task = self.task_repository.get_by_id(task_id)

        if task is None:
            raise ValueError(f"Task with id {task_id} not found")
        
        if task.status == TaskStatus.COMPLETED:
            raise ValueError("Cannot update a completed task")

        return task
    
    def _apply_updates(self, task: Task, **parameters):
        other_changes = False
        status_changed = False

        for key, value in parameters.items():
            if value is not None and hasattr(task, key):
                current_value = getattr(task, key)

                if current_value != value:
                    setattr(task, key, value)

                    if key == "status":
                        status_changed = True
                    else:
                        other_changes = True

        return other_changes, status_changed
    
    def _log_changes(self, task_id: int, other_changes: bool, status_changed: bool):
        if other_changes:
            container.log_service.create_log(task_id=task_id, action="updated")

        if status_changed:
            container.log_service.create_log(task_id=task_id, action="status_changed")