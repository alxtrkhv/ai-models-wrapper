from typer import Typer

from .chat import single_message, conversation
from .view import completion_output, system_message_prompt, user_message_prompt

chat_app = Typer(name="chat")


@chat_app.command()
def ask(prompt: str):
    completion_output(single_message(prompt), prompt)


@chat_app.command()
def start():
    messages = []

    for completion, prompt in conversation(
        messages=messages,
        system_message_call=system_message_prompt,
        user_message_call=user_message_prompt,
    ):
        completion_output(completion, prompt)
