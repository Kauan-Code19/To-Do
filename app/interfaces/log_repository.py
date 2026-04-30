from abc import ABC, abstractmethod
from domain.entities.log import Log

class LogRepository(ABC):
    
    @abstractmethod
    def create(self, log: Log) -> Log:
        pass
    
    @abstractmethod
    def get_all(self) -> list[Log]:
        pass