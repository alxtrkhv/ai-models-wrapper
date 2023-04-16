from pathlib import Path


def ensure_file_exists(file_path: Path) -> None:
    if file_path.exists() is False:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()
        file_path.write_text("{}")
