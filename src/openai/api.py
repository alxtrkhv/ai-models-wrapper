import openai
from typer import echo
from keyring import get_password

from .config import OPEN_AI_KEYRING
from ..config import read_config


def get_api() -> openai.Client | None:
    org_id = read_config().open_ai.organization_id
    if org_id is None:
        echo("Please login to OpenAI API.")
        return None

    key = get_password(OPEN_AI_KEYRING, org_id)
    if key is None:
        return None

    api = openai.Client(api_key=key, organization=org_id)

    return api
