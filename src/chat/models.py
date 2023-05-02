from enum import StrEnum

from pydantic import BaseModel
from datetime import datetime


class Error(BaseModel):
    message: str
    raised_at: datetime = datetime.utcnow()


class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    content: str
    role: MessageRole


class Chat(BaseModel):
    messages: list[Message] = []
    started_at: datetime = datetime.utcnow()
    finished_at: datetime | None = None
    errors: list[Error] = []

    def finish(self):
        self.finished_at = datetime.utcnow()

    def log_exception(self, e: Exception):
        self.errors.append(Error(message=str(e)))
