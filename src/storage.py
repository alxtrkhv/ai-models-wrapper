from pathlib import Path

from pydantic import BaseModel

from .config import APP_NAME

STORAGE_PATH = Path.home() / ".local" / "share" / APP_NAME


def save(obj: BaseModel, name: str) -> bool:
    path = STORAGE_PATH / type(obj).__name__.lower() / f"{name}.json"

    ensure_file_exists(path)
    try:
        with open(path, "w") as file:
            file.write(obj.json(indent=2))

        return True
    except Exception as e:
        print(f"Error saving file:{path} | {e}")
        return False


def ensure_file_exists(file_path: Path) -> None:
    if file_path.exists() is False:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()
        file_path.write_text("{}")


def list_files(type: type):
    path = STORAGE_PATH / type.__name__.lower()  # type: ignore

    return path.iterdir()
