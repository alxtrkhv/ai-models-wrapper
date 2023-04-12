from typer import Typer

from .openai.commands import open_ai_app
from .chat.commands import chat_app
from .config import config_app


sub_apps: list[Typer] = []


sub_apps.append(open_ai_app)
sub_apps.append(chat_app)
sub_apps.append(config_app)
