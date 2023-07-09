from typer import Typer

from .openai.commands import open_ai_app
from .chat.commands import chat_app
from .config import config_app


sub_apps: list[Typer] = [
    open_ai_app,
    chat_app,
    config_app,
]
