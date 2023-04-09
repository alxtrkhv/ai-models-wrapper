from pydantic import BaseModel


class ChatConfig(BaseModel):
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.5
    max_tokens: int = 50
