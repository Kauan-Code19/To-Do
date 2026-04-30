
from app.use_cases.services.log_service import LogService
from infrastructure.repositories.sqllite_log_repository import SQLiteLogRepository
from infrastructure.repositories.sqllite_task_repository import SQLiteTaskRepository

class Container:
    def __init__(self):
        self.task_repo = SQLiteTaskRepository()
        self.log_repo = SQLiteLogRepository()
        self.log_service = LogService(self.log_repo)

container = Container()