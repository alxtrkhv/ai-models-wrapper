from importlib import import_module
from os import listdir
from sys import path

from typer import Typer

app = Typer(pretty_exceptions_show_locals=False)


def load_commands():
    commands_dir = "commands"
    path.insert(0, commands_dir)

    for file in listdir(commands_dir):
        if file.endswith(".py") and not file.startswith("__"):
            command_name = file[:-3]
            module_name = f"{commands_dir}.{command_name}"
            module = import_module(module_name)
            app.registered_commands += module.app.registered_commands


def run():
    load_commands()
    app()


if __name__ == "__main__":
    run()
