from typer import Typer

from .models import Chat
from .chat import conversation, Completion
from .view import (
    reply_output,
    system_message_prompt,
    user_message_prompt,
    save_file_prompt,
    file_list_output,
)
from ..storage.storage import save, file_list
from ..openai.api import get_api
from ..config import read_config

chat_app = Typer(name="chat")


@chat_app.command()
def ask(prompt: str):
    api = get_api()
    if api is None:
        return

    config = read_config().chat
    completion = Completion(api, config)

    reply_output(completion.without_context(prompt))


@chat_app.command()
def new():
    api = get_api()
    if api is None:
        return

    chat = Chat()

    config = read_config().chat
    completion = Completion(api, config)

    for reply in conversation(
        messages=chat.messages,
        system_message_call=system_message_prompt,
        user_message_call=user_message_prompt,
        completion_call=completion.with_context,
    ):
        reply_output(reply)

    chat.finish()

    if len(chat.messages) > 0 and save_file_prompt():
        save(chat, str(chat.started_at.replace(microsecond=0)))


@chat_app.command()
def list():
    file_list_output(file_list(Chat))
