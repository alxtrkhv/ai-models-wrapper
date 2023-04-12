from pydantic import BaseModel
from datetime import datetime


class Chat(BaseModel):
    messages: list[dict] = []
    started_at: datetime = datetime.utcnow()
    finished_at: datetime | None = None

    def finish(self):
        self.finished_at = datetime.utcnow()
