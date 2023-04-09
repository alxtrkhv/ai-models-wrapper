from typer import Typer
from rich.console import Console

from .chat import single_completion

chat_app = Typer(name="chat")
console = Console()


@chat_app.command()
def ask(question: str):
    completion = single_completion(question)
    console.print(
        f"Tokens:{completion.usage.prompt_tokens}/{completion.usage.completion_tokens}/{completion.usage.total_tokens}"  # type: ignore
    )
    console.print(f"[green]Prompt:\n[/green]{question}")  # type: ignore
    console.print(f"[cyan]Reply:\n[/cyan]{completion.choices[0].message.content}")  # type: ignore
