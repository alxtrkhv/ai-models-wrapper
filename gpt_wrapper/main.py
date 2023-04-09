from .commands import app


def run():
    app.pretty_exceptions_show_locals = False

    app()


if __name__ == "__main__":
    run()
