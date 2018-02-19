"""A basic scaffolding for a python CLI

Usage:
    commands.py download [<URL>] [-q | -d]
    commands.py -h
    commands.py -v

Options:
    -h, --help       display this message and exit
    -v, --version    display version
    -q, --quiet      set log level to WARNING [default: INFO]
    -d, --debug      set log level to DEBUG [default: INFO]
"""
import logging
import requests

from docopt import docopt
from docopt_dispatch import dispatch

from utils import set_logging_config
from settings import VERSION, DEFAULT_URL


@dispatch.on('download')
def download(url=None, **kwargs):
    # Firstofall, make sure if have some url
    url = url or DEFAULT_URL

    # Always tell the user that you are working for him
    logging.info(f"Downloading {url}...")

    try:
        # make the request, and make sure that it succeeds
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        # in case of failure, log and stop
        logging.error(err)
        raise SystemExit("Fail to download")

    # for now save text in temporary file
    with open("tmp.html", "w") as result_text:
        result_text.write(response.text)

    # return the downloaded text (for testing purpose)
    return response.text


if __name__ == '__main__':
    kwargs = docopt(__doc__)
    set_logging_config(kwargs)
    logging.debug(kwargs)
    dispatch(__doc__, version=VERSION)
