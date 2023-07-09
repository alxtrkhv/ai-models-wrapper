from pathlib import Path
from typing import Sequence
from abc import ABC, abstractmethod

from rich.status import Status
from rich.console import Console
from rich.padding import Padding
from rich.prompt import Prompt, Confirm

from typer import echo
from pydantic import BaseModel

from .models import CompletionResult, Error


class CLIConfig(BaseModel):
    you_color: str = "green"
    assistant_color: str = "cyan"
    error_color: str = "red"

    system_message_label: str = "System"
    user_message_label: str = "User"
    assistant_message_label: str = "Assistant"
    error_message_label: str = "Error"

    save_chat_text: str = "Do you want to save this chat?"
    completion_spinner_text = "Waiting for response"

    indent: int = 2


def _colorized(text: str, color: str | None):
    if color:
        result = f"[{color}]{text}[/{color}]"
    else:
        result = f"{text}"

    return result


class IView(ABC):
    @abstractmethod
    def get_system_message(self):
        return ""

    @abstractmethod
    def get_user_message(self):
        return ""

    @abstractmethod
    def message_output(self, content: str, title: str, color: str | None):
        pass

    @abstractmethod
    def file_list_output(self, files: Sequence[Path]):
        pass

    @abstractmethod
    def save_file_prompt(self) -> bool:
        return False

    @abstractmethod
    def toggle_spinner(self):
        pass

    @abstractmethod
    def reply_output(self, reply: Error | CompletionResult):
        pass


class CLIView(IView):
    def __init__(self, config: CLIConfig):
        self.config = config
        self.console = Console()
        self._spinner = self._spinner_generator()

    def get_system_message(self):
        prompt = self.config.system_message_label
        color = self.config.you_color

        return Prompt.ask(
            _colorized(prompt, color),
            default="",
            show_default=False,
        )

    def get_user_message(self):
        prompt = self.config.user_message_label
        color = self.config.you_color

        return Prompt.ask(
            _colorized(prompt, color),
            default="",
            show_default=False,
        )

    def message_output(self, content: str, title: str, color: str | None):
        indent = self.config.indent

        self.console.print(_colorized(f"{title}:", color))
        self.console.print(Padding(content, (0, 0, 1, indent)))

    def save_file_prompt(self) -> bool:
        text = self.config.save_chat_text
        color = self.config.you_color

        return Confirm.ask(_colorized(text, color))

    def file_list_output(self, files: Sequence[Path]):
        for index, file in enumerate(files):
            echo(f"[{index}] {file.stem}")

    def toggle_spinner(self):
        next(self._spinner)

    def reply_output(self, reply: Error | CompletionResult):
        if isinstance(reply, Error):
            self._error_output(reply)

        if isinstance(reply, CompletionResult):
            self._completion_output(reply)

    def _completion_output(self, completion: CompletionResult):
        usage = completion.usage
        content = completion.message.content

        self.message_output(
            content,
            self.config.assistant_message_label,
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

    def _error_output(self, error: Error):
        self.message_output(
            error.message,
            self.config.error_message_label,
            self.config.error_color,
        )

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
