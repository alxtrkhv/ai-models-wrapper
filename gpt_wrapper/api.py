import openai
from typer import echo
from keyring import get_password

from config import read_config, APP_NAME


def get_api():
    org_id = read_config().org_name
    if org_id is None:
        echo("Please login.")
        return

    api = openai
    api.organization = org_id
    api.api_key = get_password(APP_NAME, org_id)

    return api
