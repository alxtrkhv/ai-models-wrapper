from typer import Typer

from .models import Chat
from .chat import conversation, Completion
from .view import View
from ..storage.storage import save, file_list, remove, read
from ..openai.api import get_api
from ..config import read_config

chat_app = Typer(name="chat")

api = get_api()
config = read_config()
completion = Completion(api, config.chat)
view = View(config.chat.view)


@chat_app.command()
def ask(prompt: str):
    api = get_api()
    if api is None:
        return

    view.reply_output(completion.without_context(prompt))


@chat_app.command()
def new():
    if api is None:
        return

    chat = Chat()

    for reply in conversation(
        chat=chat,
        system_message_call=view.system_message_prompt,
        user_message_call=view.user_message_prompt,
        completion_call=completion.with_context,
        spinner_call=view.toggle_spinner,
    ):
        view.reply_output(reply)

    if len(chat.messages) > 0 and view.save_file_prompt():
        save(chat, str(chat.started_at.replace(microsecond=0)))


@chat_app.command()
def list():
    view.file_list_output(file_list(Chat))


@chat_app.command()
def rm(index: int):
    remove(Chat, index)


@chat_app.command()
def show(index: int):
    chat = read(Chat, index)
    if not chat:
        return

    for message in chat.messages:
        view.message_output(message.content, message.role.capitalize(), None)


@chat_app.command(name="continue")
def continue_(index: int):
    if api is None:
        return

    chat = read(Chat, index)
    if not chat:
        return

    for reply in conversation(
        chat=chat,
        system_message_call=None,
        user_message_call=view.user_message_prompt,
        completion_call=completion.with_context,
        spinner_call=view.toggle_spinner,
    ):
        view.reply_output(reply)

    if view.save_file_prompt():
        save(chat, str(chat.started_at.replace(microsecond=0)))
        remove(Chat, index)
