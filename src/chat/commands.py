from typer import Typer

from .models import Chat
from .chat import conversation, Completion
from .view import View
from ..storage.storage import save, file_list, remove, read
from ..openai.api import get_api
from ..config import read_config

chat_app = Typer(name="chat")


@chat_app.command()
def ask(prompt: str):
    api = get_api()
    if api is None:
        return

    config = read_config()
    completion = Completion(api, config.chat)
    view = View(config.chat.view)

    view.reply_output(completion.without_context(prompt))


@chat_app.command()
def new():
    api = get_api()
    if api is None:
        return

    config = read_config()
    completion = Completion(api, config.chat)
    view = View(config.chat.view)

    chat = Chat()

    for reply in conversation(
        messages=chat.messages,
        system_message_call=view.system_message_prompt,
        user_message_call=view.user_message_prompt,
        completion_call=completion.with_context,
    ):
        view.reply_output(reply)

    chat.finish()

    if len(chat.messages) > 0 and view.save_file_prompt():
        save(chat, str(chat.started_at.replace(microsecond=0)))


@chat_app.command()
def list():
    config = read_config()
    view = View(config.chat.view)

    view.file_list_output(file_list(Chat))


@chat_app.command()
def rm(index: int):
    remove(Chat, index)


@chat_app.command()
def show(index: int):
    config = read_config()
    view = View(config.chat.view)

    chat = read(Chat, index)
    if not chat:
        return

    for message in chat.messages:
        view.message_output(message.content, message.role.capitalize(), None)
