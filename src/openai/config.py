from pydantic import BaseModel

from ..chat.config import ChatConfig

OPEN_AI_KEYRING = "Open AI API"


class OpenAIConfig(BaseModel):
    organization_id: str | None = None
    chat: ChatConfig = ChatConfig()
