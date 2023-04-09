from pydantic import BaseModel

OPEN_AI_KEYRING = "Open AI API"


class OpenAIConfig(BaseModel):
    organization_id: str | None = None
