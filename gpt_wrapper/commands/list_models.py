from typer import Typer, echo

from api import get_api

app = Typer()


@app.command()
def list_models():
    api = get_api()

    if api is None:
        return

    list = api.Model.list()
    echo(list)
