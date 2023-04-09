from typer import Typer

from .openai.commands import open_ai_app
from .chat.commands import chat_app

app = Typer(pretty_exceptions_show_locals=False)

app.add_typer(open_ai_app)
app.add_typer(chat_app)


def run():
    app()


if __name__ == "__main__":
    run()
