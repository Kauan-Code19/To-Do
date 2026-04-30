from app.interfaces.log_repository import LogRepository
from domain.entities.log import Log


class LogService:
    def __init__(self, log_repository: LogRepository):
        self.log_repository = log_repository

    def create_log(self, task_id: int, action: str) -> None:
        log = Log(task_id=task_id, action=action)
        self.log_repository.create(log)
        
    def list_logs(self) -> list[Log]:
        return self.log_repository.get_all()