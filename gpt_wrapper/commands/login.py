from typer import Option, echo
from keyring import set_password

from ..config import update_config, APP_NAME


def login(
    organization_id: str = Option(..., prompt=True),
    token: str = Option(..., prompt=True, hide_input=True),
):
    update_config({"org_name": organization_id})
    set_password(APP_NAME, organization_id, token)

    echo("Logged in successfully.")
