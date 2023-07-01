from typing import Generator

from pathlib import Path

from pydantic import BaseModel, parse_file_as

from .utils import ensure_file_exists
from ..config import APP_NAME

STORAGE_PATH = Path.home() / ".local" / "share" / APP_NAME


def save(obj: BaseModel, name: str) -> bool:
    path = _path(type(obj)) / f"{name}.json"

    ensure_file_exists(path)
    try:
        with open(path, "w") as file:
            file.write(obj.json(indent=2, exclude_none=True))

        return True
    except Exception as e:
        print(f"Error saving file: {path} | {e}")
        return False


def remove(type: type, index: int):
    for i, file in enumerate(file_list(type)):
        if i == index:
            file.unlink()


def read(type: type, index: int):
    for i, path in enumerate(file_list(type)):
        if i == index:
            return parse_file_as(type, path)


def file_list(type: type):
    return _path(type).iterdir()


def _path(type: type) -> Path:
    return STORAGE_PATH / type.__name__.lower()  # type: ignore
