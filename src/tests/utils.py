import random
import string

from src.core.config import settings
from src.tests.conftest import client


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))
