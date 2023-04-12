from typer import Typer

from .registry import sub_apps

app = Typer(pretty_exceptions_show_locals=False)

for sub_app in sub_apps:
    app.add_typer(sub_app)


def run():
    app()


if __name__ == "__main__":
    run()
