import typer

from typing import Optional
from typer.colors import RED
from pydantic import ValidationError

from wwatch.schemas import Site, User
from wwatch.cli import app
from wwatch.settings import Settings


settings = Settings()


@app.command()
def register(
    url: str = typer.Argument(settings.default_url, help="Full URL of the page to watch"),
    latency: Optional[int] = typer.Option(settings.latency, min=0, help="Nb of seconds between 2 checks"),
    email: str = typer.Option(None, help="Email where to send notifications")
):
    """
    Register a new URL. When the option \033[1m--latency\033[0m is given, the system will
    check every specified number of seconds if the page as changed.
    """
    try:
        # validate input
        site = Site(url=url, latency=latency)
        typer.echo(f"Will download from {site}")

        if email is not None:
            user = User(email=email)
            typer.echo(f"Will notify {user}")
    except ValidationError as err:
        typer.secho(str(err), fg=RED, err=True)


@app.command()
def check(url: str = settings.default_url, full: bool = False):
    # validate input
    valid_url = Site(url=url)

    if full:
        typer.echo(f"Comparing full HTML for {valid_url}")
    else:
        typer.echo(f"Diff text for {valid_url}. Use \033[1m--full\033[0m to compare all HTML")


if __name__ == "__main__":
    app()
