from pathlib import Path
from typing import Generator

from rich.console import Console
from rich.padding import Padding
from rich.prompt import Prompt, Confirm

from typer import echo


you_color = "green"
you_prompt = f"[{you_color}]Prompt[/{you_color}]"

setup_prompt = f"[{you_color}]Setup[/{you_color}]"

gpt_color = "cyan"
gpt_prompt = f"[{gpt_color}]Reply:[/{gpt_color}]"


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


def completion_output(completion):
    usage = completion.usage
    content = completion.choices[0].message.content

    console.print(gpt_prompt)
    console.print(Padding(content, (0, 0, 1, indent)))

    console.print(
        Padding(
            f"{usage.prompt_tokens}/{usage.completion_tokens}/{usage.total_tokens}",
            (1, 0),
        )
    )


save_chat_text = f"[{you_color}]Do you want to save this chat?[/{you_color}]"


def save_prompt() -> bool:
    return Confirm.ask(save_chat_text)


def file_list(files: Generator[Path, None, None]):
    for index, file in enumerate(files):
        echo(f"[{index}] {file.stem}")
