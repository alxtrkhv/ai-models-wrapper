from typer import Typer, Option, Exit
from keyring import get_password, set_password, delete_password
import openai

import config

app = Typer(pretty_exceptions_show_locals=False)


@app.command("login")
def login(
    organization_id: str = Option(..., prompt=True),
    token: str = Option(..., prompt=True, hide_input=True),
):
    config.update_config({"org_name": organization_id})
    set_password(config.APP_NAME, organization_id, token)


@app.command("logout")
def logout(are_you_sure: bool = Option(..., prompt=True)):
    if are_you_sure:
        org_name = config.read_config().org_name

        if org_name is not None:
            config.update_config({"org_name": None})
            delete_password(config.APP_NAME, org_name)


@app.command("request")
def request(message: str):
    api = _setup_api()


@app.command("list_models")
def list_models():
    api = _setup_api()
    list = api.Model.list()

    print(list)


def _setup_api():
    org_id = config.read_config().org_name
    if org_id is None:
        print("Please login.")
        Exit()

    api = openai
    api.organization = org_id
    api.api_key = get_password(config.APP_NAME, org_id)

    return api


if __name__ == "__main__":
    app()
