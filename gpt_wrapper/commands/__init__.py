from .list_models import list_models
from .login import login
from .logout import logout
from .request import request

from typer import Typer

app = Typer()

app.command()(list_models)
app.command()(login)
app.command()(logout)
app.command()(request)
