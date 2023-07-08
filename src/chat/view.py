from pathlib import Path
from typing import Generator

from rich.status import Status
from rich.console import Console
from rich.padding import Padding
from rich.prompt import Prompt, Confirm

from typer import echo
from pydantic import BaseModel

from .models import CompletionResult


class ViewConfig(BaseModel):
    you_color: str = "green"
    assistant_color: str = "cyan"
    system_message_label: str = "System"
    user_message_label: str = "User"
    assistant_message_lable: str = "Assistant"
    indent: int = 2
    save_chat_text: str = "Do you want to save this chat?"
    completion_spinner_text = "Waiting for response"


def _colorized(text: str, color: str | None):
    if color:
        result = f"[{color}]{text}[/{color}]"
    else:
        result = f"{text}"

    return result


class View:
    def __init__(self, config: ViewConfig):
        self.config = config
        self.console = Console()
        self._spinner = self._spinner_generator()

    def system_message_prompt(self):
        prompt = self.config.system_message_label
        color = self.config.you_color

        return Prompt.ask(
            _colorized(prompt, color),
            default="",
            show_default=False,
        )

    def user_message_prompt(self):
        prompt = self.config.user_message_label
        color = self.config.you_color

        return Prompt.ask(
            _colorized(prompt, color),
            default="",
            show_default=False,
        )

    def reply_output(self, completion: CompletionResult):
        usage = completion.usage
        content = completion.message.content

        self.message_output(
            content,
            self.config.assistant_message_lable,
            self.config.assistant_color,
        )

        if not usage:
            return

        self.console.print(
            Padding(
                f"{usage.prompt}/{usage.completion}/{usage.total}",
                (1, 0),
            )
        )

    def save_file_prompt(
        self,
    ) -> bool:
        text = self.config.save_chat_text
        color = self.config.you_color

        return Confirm.ask(_colorized(text, color))

    def file_list_output(self, files: Generator[Path, None, None]):
        for index, file in enumerate(files):
            echo(f"[{index}] {file.stem}")

    def message_output(self, content: str, title: str, color: str | None):
        indent = self.config.indent

        self.console.print(_colorized(f"{title}:", color))
        self.console.print(Padding(content, (0, 0, 1, indent)))

    def toggle_spinner(self):
        next(self._spinner)

    def _spinner_generator(self):
        status = Status(
            spinner="simpleDots",
            status=self.config.completion_spinner_text,
            console=self.console,
        )

        while True:
            status.start()
            yield
            status.stop()
            yield
