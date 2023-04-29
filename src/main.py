from typer import Typer

from .registry import sub_apps

app = Typer(
    pretty_exceptions_show_locals=False,
    no_args_is_help=True,
)

for sub_app in sub_apps:
    app.add_typer(sub_app)


def run_cli():
    app()
