from typer import Typer

from .models import Chat
from .chat import contextless_completion, conversation, contextful_completion
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

    completion_output(contextless_completion(prompt, api), prompt)


@chat_app.command()
def new():
    api = get_api()
    if api is None:
        return

    chat = Chat()

    for completion, prompt in conversation(
        messages=chat.messages,
        system_message_call=system_message_prompt,
        user_message_call=user_message_prompt,
        completions_call=lambda messages: contextful_completion(messages, api),
    ):
        completion_output(completion, prompt)

    chat.finish()

    if save_prompt():
        save(chat, str(chat.started_at))


@chat_app.command()
def list():
    files = list_files(Chat)
    file_list(files)
