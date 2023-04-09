from typer import echo

from ..api import get_api


def list_models():
    api = get_api()

    if api is None:
        return

    list = api.Model.list()
    echo(list)
