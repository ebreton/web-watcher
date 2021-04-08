from aiohttp import ClientSession

from wwatch.downloader import download_content


async def startup(ctx):
    ctx['session'] = ClientSession()


async def shutdown(ctx):
    await ctx['session'].close()


class WorkerSettings:
    """
        WorkerSettings defines the settings to use when creating the worker,
        it's used by the arq cli
    """
    functions = [download_content]
    on_startup = startup
    on_shutdown = shutdown
