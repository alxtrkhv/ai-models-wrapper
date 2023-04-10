from rich.console import Console
from typer import prompt


system_message_request = "Setup (system message)"
user_message_request = "Prompt"


def system_message_prompt():
    return prompt(system_message_request, default="")


def user_message_prompt():
    return prompt(user_message_request, default="")


you_color = "green"
gpt_color = "cyan"

console = Console()


def completion_output(completion, prompt):
    console.line()
    console.print(f"[{you_color}]Prompt:\n[/{you_color}]{prompt}")
    console.line()

    console.print(f"[{gpt_color}]Reply:\n[/{gpt_color}]{completion.choices[0].message.content}")  # type: ignore
    console.line()

    console.print(
        f"{completion.usage.prompt_tokens}/{completion.usage.completion_tokens}/{completion.usage.total_tokens}"  # type: ignore
    )
    console.line()
