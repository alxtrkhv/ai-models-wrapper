from os import path, makedirs
from json import load, dump
from pathlib import Path

from pydantic import BaseModel

APP_NAME = "com.alxtrkhv.gpt_wrapper"
FILE_PATH = Path.home() / ".config" / APP_NAME / "config.json"


class Config(BaseModel):
    org_name: str | None


def read_config() -> Config:
    _ensure_directory_exists(FILE_PATH)

    try:
        with open(FILE_PATH, "r") as file:
            data = load(file)
    except FileNotFoundError:
        return Config()
    except Exception as e:
        print(f"Error reading config file '{FILE_PATH}': {e}")
        return Config()

    config = Config(**data)
    return config


def update_config(updated_data: dict | Config) -> bool:
    if isinstance(updated_data, Config):
        updated_data = updated_data.dict()

    current_config = read_config()

    current_config_dict = current_config.dict()
    current_config_dict.update(updated_data)
    updated_config = Config(**current_config_dict)

    try:
        with open(FILE_PATH, "a+") as file:
            dump(updated_config.dict(), file, indent=2)
    except Exception as e:
        print(f"Error updating config file '{FILE_PATH}': {e}")
        return False

    return True


def _ensure_directory_exists(file_path: str) -> None:
    dir_name = path.dirname(file_path)
    if dir_name and not path.exists(dir_name):
        makedirs(dir_name)
