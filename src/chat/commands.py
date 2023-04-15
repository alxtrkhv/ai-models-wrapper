from typer import Typer

from .models import Chat
from .chat import conversation, Completion, Message
from .view import (
    completion_output,
    system_message_prompt,
    user_message_prompt,
    save_prompt,
    file_list,
)
from ..storage import save, list_files
from ..openai.api import get_api

chat_app = Typer(name="chat")


@chat_app.command()
def ask(prompt: str):
    api = get_api()
    if api is None:
        return

    completions = Completion(api)

    completion_output(completions.contextless(prompt), prompt)


@chat_app.command()
def new():
    api = get_api()
    if api is None:
        return

    chat = Chat()
    completions = Completion(api)

    for completion, prompt in conversation(
        messages=chat.messages,
        system_message_call=system_message_prompt,
        user_message_call=user_message_prompt,
        completions_call=completions.contextful,
    ):
        completion_output(completion, prompt)

    chat.finish()

    if len(chat.messages) > 0 and save_prompt():
        save(chat, str(chat.started_at.replace(microsecond=0)))


@chat_app.command()
def list():
    files = list_files(Chat)
    file_list(files)
