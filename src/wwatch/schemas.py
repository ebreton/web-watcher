import typer

from typer.colors import MAGENTA, YELLOW
from pydantic import BaseModel, HttpUrl, EmailStr, ValidationError


class Site(BaseModel):
    url: HttpUrl
    latency: int = 0

    def __str__(self):
        return (
            f"{typer.style(self.url, fg=MAGENTA)}"
            f" every {typer.style(f'{self.latency} secs', fg=YELLOW)}"
        )


class User(BaseModel):
    email: EmailStr

    def __str__(self):
        return f"{typer.style(self.email, fg=MAGENTA)}"


def validate_email(value):
    try:
        if value is not None:
            User(email=value)
            return value
    except ValidationError as err:
        raise typer.BadParameter(str(err))


def validate_url(value):
    try:
        if value is not None:
            Site(url=value)
            return value
    except ValidationError as err:
        raise typer.BadParameter(str(err))
