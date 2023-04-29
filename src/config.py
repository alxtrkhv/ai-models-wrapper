from pathlib import Path

from pydantic import BaseModel, parse_file_as
from pydantic.utils import deep_update
from typer import Typer, echo

from .openai.config import OpenAIConfig
from .chat.config import ChatConfig
from .storage.utils import ensure_file_exists

APP_NAME = "aimw"
FILE_PATH = Path.home() / ".config" / APP_NAME / "config.json"


class Config(BaseModel):
    open_ai: OpenAIConfig = OpenAIConfig()
    chat: ChatConfig = ChatConfig()


def read_config() -> Config:
    try:
        return parse_file_as(Config, FILE_PATH)
    except FileNotFoundError:
        return Config()
    except Exception as e:
        print(f"Error reading config file '{FILE_PATH}': {e}")
        return Config()


def update_config(new_config: Config) -> bool:
    ensure_file_exists(FILE_PATH)

    updated_config = Config(
        **deep_update(
            read_config().dict(exclude_unset=True),
            new_config.dict(exclude_unset=True),
        )
    )

    try:
        with open(FILE_PATH, "w") as file:
            file.write(updated_config.json(exclude_unset=True, indent=2))
    except Exception as e:
        print(f"Error updating config file '{FILE_PATH}': {e}")
        return False

    return True


config_app = Typer(name="config")


@config_app.command()
def list():
    echo(read_config().json(indent=2))
