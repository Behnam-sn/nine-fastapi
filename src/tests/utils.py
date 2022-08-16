import random
import string

from src.core.config import settings
from src.tests.conftest import client


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def create_random_user(username: str, password: str):
    data = {
        "username": username,
        "name": random_lower_string(),
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
        f"{settings.API_V1_STR}/auth/signin",
        data=data
    )
    tokens = response.json()

    auth_token = tokens["access_token"]
    return {"Authorization": f"Bearer {auth_token}"}


def create_random_post(token, text: str = random_lower_string()):
    data = {
        "text": text
    }

    response = client.post(
        f"{settings.API_V1_STR}/posts/",
        headers=token,
        json=data
    )

    return response.json()


def create_random_comment(token, post_id: int, text: str = random_lower_string()):
    data = {
        "text": text,
        "post_id": post_id
    }

    response = client.post(
        f"{settings.API_V1_STR}/comments/",
        headers=token,
        json=data
    )

    return response.json()


def like_post(token, post_id: int):
    response = client.post(
        f"{settings.API_V1_STR}/likes/post/{post_id}",
        headers=token,
    )

    return response.json()


def unlike_post(token, post_id: int):
    response = client.delete(
        f"{settings.API_V1_STR}/likes/post/{post_id}",
        headers=token,
    )

    return response.json()


def like_comment(token, comment_id: int):
    response = client.post(
        f"{settings.API_V1_STR}/likes/comment/{comment_id}",
        headers=token,
    )

    return response.json()


def unlike_comment(token, comment_id: int):
    response = client.delete(
        f"{settings.API_V1_STR}/likes/comment/{comment_id}",
        headers=token,
    )

    return response.json()


def follow_user(token, following_id: int):
    response = client.post(
        f"{settings.API_V1_STR}/follows/{following_id}",
        headers=token,
    )

    return response.json()
