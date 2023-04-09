from pydantic import BaseModel


class ChatConfig(BaseModel):
    model: str = "gpt-3.5-turbo"
    temperature: float = 1
    top_p: float = 1
