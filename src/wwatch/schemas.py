import typer

from typer.colors import MAGENTA, YELLOW
from pydantic import BaseModel, HttpUrl, EmailStr


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
