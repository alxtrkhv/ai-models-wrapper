from typer import Typer

from .openai.commands import open_ai_app

app = Typer(pretty_exceptions_show_locals=False)

app.add_typer(open_ai_app)


def run():
    app()


if __name__ == "__main__":
    run()
