from typing import Callable, Any

from .models import Message, MessageRole
from ..config import ChatConfig


class Completion:
    def __init__(self, api, config: ChatConfig):
        self.api = api
        self.config = config

    def without_context(self, input: str):
        return self.with_context([Message(content=input, role=MessageRole.USER)])

    def with_context(self, messages: list[Message]):
        completion = self.api.ChatCompletion.create(
            model=self.config.model,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            messages=list(map(lambda x: x.dict(), messages)),
        )

        return completion


def conversation(
    messages: list[Message],
    system_message_call: Callable[..., str],
    user_message_call: Callable[..., str],
    completion_call: Callable[[list[Message]], Any],
    spinner_call: Callable[..., None],
):
    system_message = system_message_call()
    if system_message:
        messages.append(Message(content=system_message, role=MessageRole.SYSTEM))

    while True:
        user_message = user_message_call()
        if not user_message:
            break

        messages.append(Message(content=user_message, role=MessageRole.USER))

        if spinner_call:
            spinner_call()

        reply = completion_call(messages)
        messages.append(Message(**reply.choices[0].message))

        if spinner_call:
            spinner_call()

        yield reply
