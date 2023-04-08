from typer import Typer, Option
from keyring import get_password, set_password, delete_password

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
            delete_password(config.APP_NAME, org_name)


if __name__ == "__main__":
    app()
