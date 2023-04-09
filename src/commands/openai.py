from typer import Typer, Option, echo
from keyring import delete_password, set_password
from ..config import read_config, update_config, APP_NAME


app = Typer(name="openai")


@app.command()
def login(
    organization_id: str = Option(..., prompt=True),
    token: str = Option(..., prompt=True, hide_input=True),
):
    update_config({"org_name": organization_id})
    set_password(APP_NAME, organization_id, token)

    echo("Logged in successfully.")


@app.command()
def logout(are_you_sure: bool = Option(..., prompt=True)):
    if are_you_sure is False:
        echo("Skipping logout.")
        return

    org_name = read_config().org_name

    if org_name is None:
        return

    update_config({"org_name": None})
    delete_password(APP_NAME, org_name)

    echo("Logged out successfully.")
