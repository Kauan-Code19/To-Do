import datetime
from typing import Optional

from domain.enums.task_status import TaskStatus


class Task:
    def __init__(
        self,
        title: str,
        priority: int,
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.PENDING,
    ):
        self.id: Optional[int] = None
        self.title = title
        self.description = description
        self.priority = self.__validate_priority(priority)
        self.status = status
        self.creation_date = datetime.datetime.now()
        self.deadline: Optional[datetime.datetime] = None
        self.completion_date: Optional[datetime.datetime] = None

    def __validate_priority(self, priority: int) -> int:
        if not (1 <= priority <= 5):
            raise ValueError("Priority must be between 1 and 5")
        return priority