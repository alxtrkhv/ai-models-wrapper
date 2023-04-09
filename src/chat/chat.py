from enum import StrEnum

from ..config import read_config
from ..openai.api import get_api


class ChatRoles(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


def single_completion(prompt: str):
    api = get_api()

    if api is None:
        return

    config = read_config().chat

    completion = api.ChatCompletion.create(
        model=config.model,
        temperature=config.temperature,
        top_p=config.top_p,
        messages=[
            {
                "role": ChatRoles.USER,
                "content": prompt,
            }
        ],
    )

    return completion
