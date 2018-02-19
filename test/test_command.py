import os
import pytest
import requests_mock

from commands import download, save, check_identical, url_to_filename
from settings import TEST_PATH, DEFAULT_DIFF_FILE


@pytest.fixture
def reference():
    reference_path = os.path.join(TEST_PATH, 'reference.html')
    with open(reference_path) as reference_file:
        return reference_file.read()


def test_filename():
    assert url_to_filename("http://my.test.com") == "my.test.com.html"
    assert url_to_filename("http://my.test.com/") == "my.test.com.html"
    assert url_to_filename("http://my.test.com/download") == "download.html"
    assert url_to_filename("http://my.test.com/my/download.html") == "download.html"
    assert url_to_filename("my.test.com/download.zip?format=zip") == "download.zip"


def test_download(reference):
    url = "http://my.test.com/download.html"
    downloaded = os.path.join(TEST_PATH, 'first_download.html')
    with requests_mock.Mocker() as mocker, open(downloaded) as page:
        mocker.get(url, text=page.read())
        assert download(url) == reference


def test_save(reference):
    url = "http://my.test.com/download.html"
    filename = url_to_filename(url)
    downloaded = os.path.join(TEST_PATH, 'first_download.html')
    with requests_mock.Mocker() as mocker, open(downloaded) as page:
        mocker.get(url, text=page.read())
        assert save(url) == filename
        assert os.path.exists(filename)
    # clean up a bit
    os.remove(filename)


def test_check(reference):
    url = "http://my.test.com/download.html"
    filename = url_to_filename(url)
    downloaded = os.path.join(TEST_PATH, 'first_download.html')
    changed = os.path.join(TEST_PATH, 'second_download.html')
    with requests_mock.Mocker() as mocker, open(downloaded) as page:
        mocker.get(url, text=page.read())
        # first save the file
        save(url)
        # then check identical one
        assert check_identical(url)
    # check modifications
    with requests_mock.Mocker() as mocker, open(changed) as page:
        mocker.get(url, text=page.read())
        assert not check_identical(url)
    # clean up a bit
    os.remove(filename)
    os.remove(DEFAULT_DIFF_FILE)
