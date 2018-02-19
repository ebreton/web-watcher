import os

from utils import get_optional_env


VERSION = "0.1.1"

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_PATH = os.path.join(ROOT_PATH, 'src')
TEST_PATH = os.path.join(ROOT_PATH, 'test')
REFERENCES_PATH = os.path.join(ROOT_PATH, 'references')

DEFAULT_URL = get_optional_env('DEFAULT_URL', '')
DEFAULT_HEADERS = {'Accept': 'text/html', 'User-Agent': 'Python/Requests'}

DEFAULT_DIFF_FILE = "diff_file.html"
DEFAULT_INDENTATION = 2
DEFAULT_LINE_LENGTH = 80
