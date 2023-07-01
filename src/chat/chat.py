from typing import Callable, Any, TypeAlias

from .models import Message, MessageRole, Chat, CompletionResult, CompletionUsage
from ..config import ChatConfig


ReturnCompletion: TypeAlias = Callable[[list[Message]], CompletionResult]
ReturnString: TypeAlias = Callable[..., str]
ReturnVoid: TypeAlias = Callable[..., None]


class Completion:
    def __init__(self, api, config: ChatConfig):
        self.api = api
        self.config = config

    def without_context(self, input: str):
        return self.with_context([Message(content=input, role=MessageRole.USER)])

    def with_context(self, messages: list[Message]):
        completion = self.api.ChatCompletion.create(
            model=self.config.model,
            messages=list(map(lambda x: x.dict(exclude_none=True), messages)),
        )
        usage = completion.usage

        return CompletionResult(
            message=Message(**completion.choices[0].message),
            usage=CompletionUsage(
                prompt=usage.prompt_tokens,
                completion=usage.completion_tokens,
                total=usage.total_tokens,
            ),
        )


def conversation(
    chat: Chat,
    system_message_call: ReturnString | None,
    user_message_call: ReturnString,
    completion_call: ReturnCompletion,
    spinner_call: ReturnVoid | None,
):
    if system_message_call:
        system_message = system_message_call()
        if system_message:
            chat.messages.append(
                Message(content=system_message, role=MessageRole.SYSTEM)
            )

    while True:
        user_message = user_message_call()
        if not user_message:
            break

        chat.messages.append(Message(content=user_message, role=MessageRole.USER))

        if spinner_call:
            spinner_call()

        try:
            reply = completion_call(chat.messages)

        except Exception as e:
            chat.log_exception(e)
            break

        finally:
            if spinner_call:
                spinner_call()

        chat.messages.append(reply.message)

        yield reply

    chat.finish()
