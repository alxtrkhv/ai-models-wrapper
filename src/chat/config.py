from enum import StrEnum

from pydantic import BaseModel


class ChatModels(StrEnum):
    GPT3 = "gpt-3.5-turbo"
    GPT4 = "gpt-4"
    GPT4_LARGE = "gpt-4-32k"
    GPT4_TURBO = "gpt-4-turbo-preview"
    GPT4_1106_PREVIEW = "gpt-4-1106-preview"


class ChatConfig(BaseModel):
    model: ChatModels = ChatModels.GPT4_1106_PREVIEW
