from typer import Typer
from rich.console import Console

from .chat import get_response

chat_app = Typer(name="chat")
console = Console()


@chat_app.command()
def ask(question: str):
    answer = get_response(question)
    console.print(f"[green]You:[/green] {question}")
    console.print(f"[cyan]GPT:[/cyan] {answer}")
