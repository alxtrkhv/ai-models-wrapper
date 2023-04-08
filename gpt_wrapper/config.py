from os import open
from json import load, dump

from pydantic import BaseModel

APP_NAME = "com.alxtrkhv.gpt_wrapper"
FILE_PATH = f"~/.config/{APP_NAME}"


class AppConfig(BaseModel):
    org_name: str


with open(FILE_PATH, "r") as file:
    app_config = load(file)


def update(new_values: dict):
    values = app_config.dict()
    values.update(new_values)

    with open(FILE_PATH, "w") as file:
        dump(values, file)
