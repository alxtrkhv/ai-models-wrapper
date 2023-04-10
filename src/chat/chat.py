from enum import StrEnum
from typing import Callable

from ..config import read_config
from ..openai.api import get_api


class MessageRole(StrEnum):
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
        messages.append(message(MessageRole.SYSTEM, system_message))

    while True:
        user_message = user_message_call()
        if not user_message:
            break

        messages.append(message(MessageRole.USER, user_message))

        yield (contextful_completion(messages), user_message)


def contextless_completion(message: str):
    return contextful_completion([{"role": MessageRole.USER, "content": message}])


def contextful_completion(messages: list):
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


def message(role: MessageRole, content: str):
    return {"role": role, "content": content}
