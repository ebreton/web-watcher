from typing import Set

from pydantic import (
    BaseSettings,
    PyObject,
    RedisDsn,
    PostgresDsn,
    Field,
)
from pydantic.networks import HttpUrl
from wwatch.schemas import Site


class Settings(BaseSettings):
    """
    {
        'auth_key': 'xxx',
        'api_key': 'xxx',
        'redis_dsn': RedisDsn('redis://user:pass@localhost:6379/1',
    scheme='redis', user='user', password='pass', host='localhost',
    host_type='int_domain', port='6379', path='/1'),
        'pg_dsn': PostgresDsn('postgres://user:pass@localhost:5432/foobar',
    scheme='postgres', user='user', password='pass', host='localhost',
    host_type='int_domain', port='5432', path='/foobar'),
        'special_function': <built-in function cos>,
        'domains': set(),
        'site': {'url': 'https://typer.tiangolo.com', 'latency': 0}
    }
    """
    auth_key: str
    api_key: str = Field(..., env='api_key')

    redis_dsn: RedisDsn = 'redis://user:pass@localhost:6379/1'
    pg_dsn: PostgresDsn = 'postgres://user:pass@localhost:5432/foobar'

    special_function: PyObject = 'math.cos'

    # to override domains:
    # export watcher_domains='["foo.com", "bar.com"]'
    domains: Set[str] = set()

    # to override site:
    # export watcher_site='{"url": "x", "latency": 1}'
    site: Site

    default_url: HttpUrl
    latency: int = 0

    class Config:

        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = 'watcher_'  # defaults to no prefix, i.e. ""
        fields = {
            'auth_key': {
                'env': 'auth_key',
            },
            'redis_dsn': {
                'env': ['service_redis_dsn', 'redis_url']
            }
        }
