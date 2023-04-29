from pathlib import Path
from typing import Generator

from rich.console import Console
from rich.padding import Padding
from rich.prompt import Prompt, Confirm

from typer import echo


you_color = "green"
you_prompt = f"[{you_color}]User[/{you_color}]"

setup_prompt = f"[{you_color}]System[/{you_color}]"

gpt_color = "cyan"
gpt_prompt = f"[{gpt_color}]Assistant:[/{gpt_color}]"


indent = 2

console = Console()


def system_message_prompt():
    return Prompt.ask(
        setup_prompt,
        default="",
        show_default=False,
    )


def user_message_prompt():
    return Prompt.ask(
        you_prompt,
        default="",
        show_default=False,
    )


def message_output(message, title):
    console.print(title)
    console.print(Padding(message, (0, 0, 1, indent)))


def reply_output(completion):
    usage = completion.usage
    content = completion.choices[0].message.content

    message_output(content, gpt_prompt)

    console.print(
        Padding(
            f"{usage.prompt_tokens}/{usage.completion_tokens}/{usage.total_tokens}",
            (1, 0),
        )
    )


save_chat_text = f"[{you_color}]Do you want to save this chat?[/{you_color}]"


def save_file_prompt() -> bool:
    return Confirm.ask(save_chat_text)


def file_list_output(files: Generator[Path, None, None]):
    for index, file in enumerate(files):
        echo(f"[{index}] {file.stem}")
