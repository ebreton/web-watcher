import os

from utils import get_optional_env


VERSION = "0.1.1"

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_PATH = os.path.join(ROOT_PATH, 'src')
TEST_PATH = os.path.join(ROOT_PATH, 'test')

DEFAULT_URL = get_optional_env('DEFAULT_URL', '')
