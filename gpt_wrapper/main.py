from typer import Typer
from rich.prompt import Prompt
from keyring import get_password, set_password, delete_password

import config

app = Typer()


@app.command("login")
def login():
    org_name = Prompt.ask("Enter organisation name")
    token = Prompt.ask("Enter token", password=True)

    config.update_config({"org_name": org_name})

    set_password(config.APP_NAME, org_name, token)


@app.command("logout")
def logout():
    should_logout = Prompt.ask("Are you sure you want to logout?", choices=["y", "n"])

    if should_logout == "y":
        org_name = config.read_config().org_name

        if org_name is not None:
            delete_password(config.APP_NAME, org_name)


if __name__ == "__main__":
    app()
