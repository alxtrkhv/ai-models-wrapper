from json import load
from pathlib import Path

from pydantic import BaseModel
from pydantic.utils import deep_update
from typer import Typer, echo

from .openai.config import OpenAIConfig
from .chat.config import ChatConfig

APP_NAME = "aimw"
FILE_PATH = Path.home() / ".config" / APP_NAME / "config.json"


class Config(BaseModel):
    open_ai: OpenAIConfig = OpenAIConfig()
    chat: ChatConfig = ChatConfig()


def read_config() -> Config:
    try:
        with open(FILE_PATH, "r") as file:
            data = load(file)
    except FileNotFoundError:
        return Config()  # type: ignore
    except Exception as e:
        print(f"Error reading config file '{FILE_PATH}': {e}")
        return Config()  # type: ignore

    config = Config(**data)
    return config


def update_config(updated_data: dict | Config) -> bool:
    if FILE_PATH.exists() is False:
        FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        FILE_PATH.touch()
        FILE_PATH.write_text("{}")

    if isinstance(updated_data, Config):
        updated_data = updated_data.dict()

    updated_config = Config(
        **deep_update(read_config().dict(exclude_unset=True), updated_data)
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
