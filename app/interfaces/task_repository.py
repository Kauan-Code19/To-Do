from abc import ABC, abstractmethod

from domain.entities.task import Task

class TaskRepository(ABC):

    @abstractmethod
    def create(self, task: Task) -> Task:
        pass
    
    @abstractmethod
    def get_all(self) -> list[Task]:
        pass