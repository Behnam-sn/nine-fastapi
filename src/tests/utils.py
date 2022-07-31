import random
import string

from src.core.config import settings
from src.tests.conftest import client


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def create_random_user(username: str = random_lower_string(), name: str = random_lower_string(), password: str = random_lower_string()):
    data = {
        "username": username,
        "name": name,
        "password": password
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json=data
    )

    return response.json()


def user_authentication_headers(username: str, password: str):
    data = {
        "username": username,
        "password": password
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=data
    )
    tokens = response.json()

    auth_token = tokens["access_token"]
    return {"Authorization": f"Bearer {auth_token}"}


def create_random_post(text: str = random_lower_string()):
    data = {
        "text": text,
    }

    response = client.post(
        f"{settings.API_V1_STR}/items/",
        json=data
    )

    return response.json()
