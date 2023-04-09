from typer import Typer, Option, echo
from keyring import delete_password, set_password

from .config import OPEN_AI_KEYRING
from ..config import read_config, update_config


open_ai_app = Typer(name="openai")


@open_ai_app.command()
def login(
    organization_id: str = Option(..., prompt=True),
    token: str = Option(..., prompt=True, hide_input=True),
):
    update_config({"open_ai": {"organization_id": organization_id}})
    set_password(OPEN_AI_KEYRING, organization_id, token)

    echo("Logged in successfully.")


@open_ai_app.command()
def logout(are_you_sure: bool = Option(..., prompt=True)):
    if are_you_sure is False:
        echo("Skipping logout.")
        return

    organization_id = read_config().open_ai.organization_id

    if organization_id is None:
        return

    update_config({"open_ai": {"organization_id": None}})
    delete_password(OPEN_AI_KEYRING, organization_id)

    echo("Logged out successfully.")
