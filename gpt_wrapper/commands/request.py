from typer import Typer

from api import get_api

app = Typer()


@app.command("request")
def request(message: str):
    api = get_api()
