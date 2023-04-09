from typer import Typer

from .commands import openai

app = Typer(pretty_exceptions_show_locals=False)
app.add_typer(openai.app)


def run():
    app()


if __name__ == "__main__":
    run()
