from .view import IView
from .models import Message, MessageRole, Chat, CompletionResult, CompletionUsage, Error
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


def conversation(chat: Chat, completion: Completion, view: IView):
    system_message = view.get_system_message()
    if system_message:
        chat.messages.append(
            Message(content=system_message, role=MessageRole.SYSTEM)
        )

    while True:
        user_message = view.get_user_message()
        if not user_message:
            break

        chat.messages.append(Message(content=user_message, role=MessageRole.USER))

        view.toggle_spinner()

        try:
            reply = completion.with_context(chat.messages)

        except Exception as e:
            chat.log_exception(e)
            yield Error(message=str(e))
            break

        finally:
            view.toggle_spinner()

        chat.messages.append(reply.message)

        yield reply

    chat.finish()
