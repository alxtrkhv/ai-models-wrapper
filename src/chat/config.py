from enum import Enum

from pydantic import BaseModel


class ChatModels(str, Enum):
    GPT3 = "gpt-3.5-turbo"
    GPT3_LARGE = "gpt-3.5-turbo-16k"
    GPT4 = "gpt-4"
    GPT4_LARGE = "gpt-4-32k"
    GPT4_TURBO = "gpt-4-1106-preview"


class ChatConfig(BaseModel):
    model: ChatModels = ChatModels.GPT4
