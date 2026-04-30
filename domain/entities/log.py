from datetime import datetime
from typing import Optional

class Log:
    def __init__(self, task_id: int, action: str):
        self.id: Optional[int] = None
        self.task_id = task_id
        self.action = action
        self.date = datetime.now()