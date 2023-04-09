from typer import Typer, prompt
from rich.console import Console

from .chat import single_message, ChatRoles, multiple_messages

chat_app = Typer(name="chat")
console = Console()


@chat_app.command()
def ask(prompt: str):
    completion = single_message(prompt)
    output(prompt, completion)


@chat_app.command()
def start():
    messages = []

    system_message = prompt("System message", default="")
    if len(system_message) > 0:
        messages.append({"role": ChatRoles.SYSTEM, "content": system_message})

    while True:
        message = prompt("Prompt", default="")
        if len(message) > 0:
            messages.append({"role": ChatRoles.USER, "content": message})
        else:
            break

        completion = multiple_messages(messages)
        messages.append(completion.choices[0].message)  # type: ignore

        output(message, completion)


def output(prompt, completion):
    console.print(f"[green]Prompt:\n[/green]{prompt}")
    console.line()

    console.print(f"[cyan]Reply:\n[/cyan]{completion.choices[0].message.content}")  # type: ignore
    console.line()
    console.print(
        f"{completion.usage.prompt_tokens}/{completion.usage.completion_tokens}/{completion.usage.total_tokens}"  # type: ignore
    )
    console.line()
