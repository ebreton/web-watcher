import typer

from typing import Optional

from wwatch.schemas import Site, User, validate_email, validate_url
from wwatch.cli import app
from wwatch.settings import Settings


settings = Settings()


@app.command()
def register(
    url: str = typer.Argument(settings.default_url, help="Full URL of the page to watch", callback=validate_url),
    latency: Optional[int] = typer.Option(settings.latency, min=0, help="Nb of seconds between 2 checks"),
    email: str = typer.Option(None, help="Email where to send notifications", callback=validate_email),
):
    """
    Register a new URL. When the option \033[1m--latency\033[0m is given, the system will
    check every specified number of seconds if the page as changed.
    """
    to_register = Site(url=url, latency=latency)
    typer.echo(f"Will download from {to_register}")

    if email is not None:
        user = User(email=email)
        typer.echo(f"Will notify {user}")


@app.command()
def check(
    url: str = typer.Option(settings.default_url, callback=validate_url),
    full: bool = False,
):
    """
        Check whether the given url has changed.
        Compare base on HTML if \033[1m--full\033[0m is given, otherwise on plain text
    """
    to_check = Site(url=url)

    if full:
        typer.echo(f"Comparing full HTML for {to_check}")
    else:
        typer.echo(f"Diff text for {to_check}. Use \033[1m--full\033[0m to compare all HTML")


@app.command('list')
def list_by(
    email: str = typer.Option(None, help="Filter list with email (if provided)", callback=validate_email)
):
    """
        List Web Watchers listed in the system. Filter by email if any provided
    """
    typer.echo("Listing")


if __name__ == "__main__":
    app()
