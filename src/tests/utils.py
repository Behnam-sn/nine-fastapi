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
    tokens = response.json()

    auth_token = tokens["access_token"]
    return {"Authorization": f"Bearer {auth_token}"}


def get_random_user(username: str):
    response = client.get(
        f"{settings.API_V1_STR}/users/{username}",
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


def deactive_user(username: str, token: str):
    client.put(
        f"{settings.API_V1_STR}/users/deactivate/{username}",
        headers=token,
    )


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


def deactive_post(id: int, token: str):
    client.put(
        f"{settings.API_V1_STR}/posts/deactivate/{id}",
        headers=token,
    )


def all_active_posts_count():
    response = client.get(
        f"{settings.API_V1_STR}/posts/count/",
    )
    return response.json()


def all_active_posts_ids(count: int):
    response = client.get(
        f"{settings.API_V1_STR}/posts/ids/?limit={count + 10}",
    )
    return response.json()


def active_posts_count_by_owner_id(owner_id: int):
    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/count/{owner_id}",
    )
    return response.json()


def active_posts_ids_by_owner_id(owner_id: int):
    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/ids/{owner_id}",
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


def deactive_comment(id: int, token: str):
    client.put(
        f"{settings.API_V1_STR}/comments/deactivate/{id}",
        headers=token,
    )


def all_active_comments_count():
    response = client.get(
        f"{settings.API_V1_STR}/comments/count/",
    )
    return response.json()


def all_active_comments_ids(count: int):
    response = client.get(
        f"{settings.API_V1_STR}/comments/ids/?limit={count + 10}",
    )
    return response.json()


def active_comments_count_by_owner_id(owner_id: int):
    response = client.get(
        f"{settings.API_V1_STR}/comments/owner/count/{owner_id}",
    )
    return response.json()


def active_comments_ids_by_owner_id(owner_id: int):
    response = client.get(
        f"{settings.API_V1_STR}/comments/owner/ids/{owner_id}",
    )
    return response.json()


def active_comments_count_by_post_id(post_id: int):
    response = client.get(
        f"{settings.API_V1_STR}/comments/post/count/{post_id}",
    )
    return response.json()


def active_comments_ids_by_post_id(post_id: int):
    response = client.get(
        f"{settings.API_V1_STR}/comments/post/ids/{post_id}",
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
