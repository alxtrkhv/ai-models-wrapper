from typer import Typer, Option
from keyring import delete_password

from config import read_config, update_config, APP_NAME

app = Typer()


@app.command("logout")
def logout(are_you_sure: bool = Option(..., prompt=True)):
    if are_you_sure is False:
        return

    org_name = read_config().org_name

    if org_name is None:
        return

    update_config({"org_name": None})
    delete_password(APP_NAME, org_name)
