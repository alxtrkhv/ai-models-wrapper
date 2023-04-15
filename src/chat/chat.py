from typing import Callable, Any

from .models import Message, MessageRole
from ..config import read_config


class Completion:
    def __init__(self, api):
        self.api = api

    def contextless(self, input: str):
        return self.contextful([Message(content=input, role=MessageRole.USER)])

    def contextful(self, messages: list[Message]):
        config = read_config().chat

        completion = self.api.ChatCompletion.create(
            model=config.model,
            temperature=config.temperature,
            top_p=config.top_p,
            messages=list(map(lambda x: x.dict(), messages)),
        )

        return completion


def conversation(
    messages: list[Message],
    system_message_call: Callable[..., str],
    user_message_call: Callable[..., str],
    completions_call: Callable[[list[Message]], Any],
):
    system_message = system_message_call()
    if system_message:
        messages.append(Message(content=system_message, role=MessageRole.SYSTEM))

    while True:
        user_message = user_message_call()
        if not user_message:
            break

        messages.append(Message(content=user_message, role=MessageRole.USER))

        completion = completions_call(messages)
        messages.append(completion.choices[0].message)  # type: ignore

        yield (completion, user_message)
