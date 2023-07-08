from enum import Enum

from pydantic import BaseModel


class ChatModels(str, Enum):
    GPT3 = "gpt-3.5-turbo"
    GPT3_LARGE = "gpt-3.5-turbo-16k"
    GPT4 = "gpt-4"


class ChatConfig(BaseModel):
    model: ChatModels = ChatModels.GPT3_LARGE
