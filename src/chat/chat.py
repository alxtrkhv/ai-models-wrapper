from enum import StrEnum
from typing import Callable

from ..config import read_config
from ..openai.api import get_api


class ChatRoles(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


def conversation(
    messages: list[dict],
    system_message_call: Callable[..., str],
    user_message_call: Callable[..., str],
):
    system_message = system_message_call()
    if system_message:
        messages.append({"role": ChatRoles.SYSTEM, "content": system_message})

    while True:
        message = user_message_call()
        if not message:
            break

        messages.append({"role": ChatRoles.USER, "content": message})

        yield (multiple_messages(messages), message)


def single_message(message: str):
    return multiple_messages([{"role": ChatRoles.USER, "content": message}])


def multiple_messages(messages: list):
    api = get_api()

    if api is None:
        return

    config = read_config().chat

    completion = api.ChatCompletion.create(
        model=config.model,
        temperature=config.temperature,
        top_p=config.top_p,
        messages=messages,
    )

    return completion
