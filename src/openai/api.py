import openai
from typer import echo
from keyring import get_password

from .config import OPEN_AI_KEYRING
from ..config import read_config


def get_api():
    org_id = read_config().open_ai.organization_id
    if org_id is None:
        echo("Please login to OpenAI API.")
        return

    api = openai
    api.organization = org_id
    api.api_key = get_password(OPEN_AI_KEYRING, org_id)

    return api
