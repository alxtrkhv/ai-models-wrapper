from openai import Client
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_tool_message_param import (
    ChatCompletionToolMessageParam,
)
from openai.types.chat.chat_completion_user_message_param import (
    ChatCompletionUserMessageParam,
)
from openai.types.chat.chat_completion_system_message_param import (
    ChatCompletionSystemMessageParam,
)
from openai.types.chat.chat_completion_function_message_param import (
    ChatCompletionFunctionMessageParam,
)
from openai.types.chat.chat_completion_assistant_message_param import (
    ChatCompletionAssistantMessageParam,
)

from .view import View
from .models import Message, MessageRole, Chat, CompletionResult, CompletionUsage, Error
from ..config import ChatConfig


class Completion:
    def __init__(self, api: Client, config: ChatConfig):
        self.api = api
        self.config = config

    def without_context(self, input: str):
        return self.with_context([Message(content=input, role=MessageRole.USER)])

    def with_context(self, messages: list[Message]):
        completion = self.api.chat.completions.create(
            model=self.config.model,
            messages=list(map(_parse_message, messages)),
        )
        usage = (
            CompletionUsage(
                prompt=completion.usage.prompt_tokens,
                completion=completion.usage.completion_tokens,
                total=completion.usage.total_tokens,
            )
            if completion.usage is not None
            else None
        )

        choice = completion.choices[0].message

        message = Message(
            content=choice.content,
            role=MessageRole[choice.content if choice.content is not None else "none"],
        )

        return CompletionResult(
            message=message,
            usage=usage,
        )


def conversation(chat: Chat, completion: Completion, view: View):
    system_message = view.get_system_message()
    if system_message:
        chat.messages.append(Message(content=system_message, role=MessageRole.SYSTEM))

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


def _parse_message(message: Message) -> ChatCompletionMessageParam:
    result = None

    match message.role:
        case MessageRole.USER:
            result = ChatCompletionUserMessageParam(content=message.content)


    return result
