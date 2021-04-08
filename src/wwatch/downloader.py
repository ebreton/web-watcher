
import asyncio

from aiohttp import ClientSession
from typing import List
from pydantic import HttpUrl
from devtools import debug
from arq import create_pool
from arq.connections import RedisSettings
from wwatch.schemas import Site


async def download_content(ctx, url: HttpUrl):
    session: ClientSession = ctx['session']
    async with session.get(url) as response:
        content = await response.text()
        debug(f'{url}: {content:.80}...')
    return len(content)


async def queue(task: str, sites: List[Site]):
    redis = await create_pool(RedisSettings())
    for site in sites:
        await redis.enqueue_job(task, site.url)


def add_sites(sites: List[Site]):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(queue('download_content', sites))
