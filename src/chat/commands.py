from typer import Typer, Option

from .models import Chat
from .chat import conversation, Completion
from .view import View
from .config import ChatModels, ViewConfig
from ..storage import storage
from ..openai.api import get_api
from ..config import read_config

chat_app = Typer(
    name="chat",
    no_args_is_help=True,
)

api = get_api()
config = read_config()
completion = Completion(api, config.chat)
view = View(ViewConfig())


@chat_app.callback()
def callback(model: ChatModels = Option(None)):
    if model:
        config.chat.model = model


@chat_app.command()
def ask(prompt: str):
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
        storage.save(chat, str(chat.started_at.replace(microsecond=0)))


@chat_app.command()
def list():
    view.file_list_output(storage.file_list(Chat))


@chat_app.command()
def remove(index: int):
    storage.remove(Chat, index)


@chat_app.command()
def show(index: int):
    chat = storage.read(Chat, index)
    if not chat:
        return

    for message in chat.messages:
        view.message_output(message.content, message.role.capitalize(), None)


@chat_app.command(name="continue")
def continue_(index: int):
    if api is None:
        return

    chat = storage.read(Chat, index)
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
        storage.save(chat, str(chat.started_at.replace(microsecond=0)))
        storage.remove(Chat, index)
