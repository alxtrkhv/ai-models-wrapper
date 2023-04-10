from rich.console import Console
from typer import prompt

you_color = "green"
gpt_color = "cyan"

console = Console()


def system_message_prompt():
    return prompt("Setup (system message)", default="")


def user_message_prompt():
    return prompt("Prompt:", default="")


def completion_output(completion, prompt):
    console.print(f"[{you_color}]Prompt:\n[/{you_color}]{prompt}")
    console.line()

    console.print(f"[{gpt_color}]Reply:\n[/{gpt_color}]{completion.choices[0].message.content}")  # type: ignore
    console.line()

    console.print(
        f"{completion.usage.prompt_tokens}/{completion.usage.completion_tokens}/{completion.usage.total_tokens}"  # type: ignore
    )
    console.line()
