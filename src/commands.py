"""A basic scaffolding for a python CLI

Usage:
    commands.py download [--url=URL] [-q | -d]
    commands.py save [--url=URL --base-dir=PATH] [-q | -d]
    commands.py check [--url=URL --base-dir=PATH --output-file=PATH] [-q | -d]
    commands.py -h
    commands.py -v

Options:
    -h, --help       display this message and exit
    -v, --version    display version
    -q, --quiet      set log level to WARNING [default: INFO]
    -d, --debug      set log level to DEBUG [default: INFO]
"""
import os
import logging
import requests
import posixpath
import difflib

from urllib.parse import urlparse
from docopt import docopt
from docopt_dispatch import dispatch

from utils import set_logging_config
from settings import VERSION, REFERENCES_PATH, DEFAULT_URL, DEFAULT_HEADERS, \
    DEFAULT_DIFF_FILE, DEFAULT_INDENTATION, DEFAULT_LINE_LENGTH


def url_to_filename(url, base_dir=''):
    parsed_url = urlparse(url)
    file_path = posixpath.basename(parsed_url.path)

    # if no basename (e.g. www.domain.com)
    if not file_path:
        file_path = f'{parsed_url.hostname}.html'

    # if no extension (e.g www.domain.com/path)
    if not os.path.splitext(file_path)[1]:
        file_path = f'{file_path}.html'

    # prefix with base_dir if given
    if base_dir:
        file_path = posixpath.join(base_dir, file_path)

    # return new name
    return file_path


@dispatch.on('download')
def download(url=None, **kwargs):
    # Firstofall, make sure if have some url
    url = url or DEFAULT_URL

    # Always tell the user that you are working for him
    logging.info(f"Downloading {url}...")

    try:
        # make the request, and make sure that it succeeds
        response = requests.get(url, headers=DEFAULT_HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        # in case of failure, log and stop
        logging.error(err)
        raise SystemExit("Fail to download")

    # return the downloaded text (for testing purpose)
    logging.info(f"Downloaded {response}...")
    return response.text


@dispatch.on('save')
def save(url=None, base_dir=None, **kwargs):
    # Firstofall, make sure if have some url
    url = url or DEFAULT_URL
    base_dir = base_dir if base_dir is not None else REFERENCES_PATH
    filename = url_to_filename(url, base_dir=base_dir)

    # download page
    downloaded = download(url=url)

    # for now save text in temporary file
    logging.info(f"Saving response to {filename}...")

    with open(filename, "w") as result_text:
        result_text.write(downloaded)

    # return the path to the saved file
    return filename


@dispatch.on('check')
def check_identical(url=None, base_dir=None, output_file=None, **kwargs):
    """ Returns:
        - True if no reference found (in this case, a reference is created)
        - True if the downloaded file is identical to the reference
        - False if there are differences between downloaded file and reference
    """
    # Firstofall, make sure if have some url
    url = url or DEFAULT_URL
    base_dir = base_dir if base_dir is not None else REFERENCES_PATH
    output_file = output_file if output_file is not None else DEFAULT_DIFF_FILE

    # Secondly, make sure if have a reference
    filename = url_to_filename(url, base_dir=base_dir)
    if not os.path.exists(filename):
        logging.info(f"Reference file {filename} not found, creating it...")
        save(url=url, base_dir=base_dir)
        # in this case, we have nothing to diff, just return
        return True

    # download latest version of page
    downloaded = download(url=url)

    # open reference for comparison
    logging.info("Comparing downloaded file with reference...")

    with open(filename) as reference, open(output_file, 'w') as output:
        # Use a comparator that will generate 'pretty' HTML
        comparator = difflib.HtmlDiff(
            tabsize=DEFAULT_INDENTATION,
            wrapcolumn=DEFAULT_LINE_LENGTH)

        # compute differences into a file
        differences = comparator.make_file(
            reference.read().splitlines(),
            downloaded.splitlines(),
            context=True)

        # Simply display a message if files are identical
        if "No Differences Found" in differences:
            logging.info("No change since last download")
            return True

        # print differences in html file
        else:
            print(differences, file=output)
            logging.info("Differences computed")
            logging.info(" => open diff_file.html to check the results")
            return False


if __name__ == '__main__':
    kwargs = docopt(__doc__)
    set_logging_config(kwargs)
    logging.debug(kwargs)
    dispatch(__doc__, version=VERSION)
