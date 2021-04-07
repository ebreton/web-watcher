import typer
import logging

from typer.colors import YELLOW, GREEN, BRIGHT_WHITE
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from devtools import debug
from wwatch.settings import Settings

__version__ = "2021.3.1"


def version_callback(value: bool):
    if value:
        typer.secho(f"Web Watcher CLI Version: {__version__}", fg=GREEN)
        raise typer.Exit()


class CustomHelpColorsGroup(HelpColorsGroup):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.help_headers_color = YELLOW
        self.help_options_color = BRIGHT_WHITE


class CustomHelpColorsCommand(HelpColorsCommand):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.help_headers_color = YELLOW
        self.help_options_color = BRIGHT_WHITE


class LootMarshalTyper(typer.Typer):

    def __init__(self, *args, cls=CustomHelpColorsGroup, **kwargs) -> None:
        super().__init__(*args, cls=cls, **kwargs)

    def command(self, *args, cls=CustomHelpColorsCommand, **kwargs) -> typer.Typer.command:
        return super().command(*args, cls=cls, **kwargs)


app = LootMarshalTyper(cls=CustomHelpColorsGroup)


@app.callback()
def parent(
    version: bool = typer.Option(False, '--version', is_eager=True, callback=version_callback, show_default=False),
    verbose: int = typer.Option(0, '--verbose', '-v', count=True),
):
    """
        Keep watch with resilience

        You may \033[32mregister\033[0m as many URLs you want to watch.
        They can be either automatically checks every given number of seconds,
        or on demand with \033[32mcheck\033[0m command
    """
    if verbose == 0:
        logging_level = logging.ERROR
    elif verbose == 1:
        logging_level = logging.WARNING
    elif verbose == 2:
        logging_level = logging.INFO
    elif verbose == 3:
        logging_level = logging.DEBUG
        debug(Settings().dict())

    logging.basicConfig(level=logging_level)
    logging.info(f"Logging level set to {logging_level}")
