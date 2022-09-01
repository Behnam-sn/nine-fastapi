import random
import string

from src.core.config import settings
from src.tests.conftest import client


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def authentication_headers(username: str, password: str):
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


def get_user(username: str):
    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/users/{username}",
        headers=superuser_token,
    )

    return response.json()


def get_active_user(username: str):
    response = client.get(
        f"{settings.API_V1_STR}/active-users/{username}",
    )

    return response.json()


def deactivate_user(username: str, token: str):
    client.put(
        f"{settings.API_V1_STR}/users/deactivate/{username}",
        headers=token,
    )


def get_all_users_count():
    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/users/count/",
        headers=superuser_token,
    )

    return response.json()


def get_all_active_users_count():
    response = client.get(
        f"{settings.API_V1_STR}/active-users/count/",
    )

    return response.json()


def create_random_post(token: str, text: str = random_lower_string()):
    data = {
        "text": text
    }

    response = client.post(
        f"{settings.API_V1_STR}/posts/",
        headers=token,
        json=data
    )

    return response.json()


# def get_post(post_id: int):
    # response = client.get(
    #     f"{settings.API_V1_STR}/posts/{post_id}",
    # )
    # return response.json()
    # pass


def get_active_post(post_id: int):
    response = client.get(
        f"{settings.API_V1_STR}/active-posts/{post_id}",
    )
    return response.json()


def deactivate_post(id: int, token: str):
    client.put(
        f"{settings.API_V1_STR}/posts/deactivate/{id}",
        headers=token,
    )


def get_all_posts_count():
    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/posts/count/",
        headers=superuser_token,
    )

    return response.json()


def get_all_posts_ids(count: int):
    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/posts/ids/?limit={count + 10}",
        headers=superuser_token,
    )

    return response.json()


def get_posts_count_by_owner_id(owner_id: int):
    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/count/{owner_id}",
        headers=superuser_token,
    )

    return response.json()


def get_posts_ids_by_owner_id(owner_id: int):
    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/ids/{owner_id}",
        headers=superuser_token,
    )

    return response.json()


def get_all_active_posts_count():
    response = client.get(
        f"{settings.API_V1_STR}/active-posts/count/",
    )
    return response.json()


def get_all_active_posts_ids(count: int):
    response = client.get(
        f"{settings.API_V1_STR}/active-posts/ids/?limit={count + 10}",
    )
    return response.json()


def get_active_posts_count_by_owner_id(owner_id: int):
    response = client.get(
        f"{settings.API_V1_STR}/active-posts/owner/count/{owner_id}",
    )
    return response.json()


def get_active_posts_ids_by_owner_id(owner_id: int):
    response = client.get(
        f"{settings.API_V1_STR}/active-posts/owner/ids/{owner_id}",
    )
    return response.json()


def create_random_comment(post_id: int, token: str, text: str = random_lower_string()):
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


def deactivate_comment(id: int, token: str):
    client.put(
        f"{settings.API_V1_STR}/comments/deactivate/{id}",
        headers=token,
    )


def get_all_comments_count():
    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/count/",
        headers=superuser_token,
    )

    return response.json()


def get_all_comments_ids(count: int):
    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/ids/?limit={count + 10}",
        headers=superuser_token,
    )

    return response.json()


def get_comments_count_by_owner_id(owner_id: int):
    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/owner/count/{owner_id}",
        headers=superuser_token,
    )

    return response.json()


def get_comments_ids_by_owner_id(owner_id: int):
    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/owner/ids/{owner_id}",
        headers=superuser_token,
    )

    return response.json()


def get_comments_count_by_post_id(post_id: int):
    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/post/count/{post_id}",
        headers=superuser_token,
    )

    return response.json()


def get_comments_ids_by_post_id(post_id: int):
    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/post/ids/{post_id}",
        headers=superuser_token,
    )

    return response.json()


def get_all_active_comments_count():
    response = client.get(
        f"{settings.API_V1_STR}/active-comments/count/",
    )
    return response.json()


def get_all_active_comments_ids(count: int):
    response = client.get(
        f"{settings.API_V1_STR}/active-comments/ids/?limit={count + 10}",
    )
    return response.json()


def get_active_comments_count_by_owner_id(owner_id: int):
    response = client.get(
        f"{settings.API_V1_STR}/active-comments/owner/count/{owner_id}",
    )
    return response.json()


def get_active_comments_ids_by_owner_id(owner_id: int):
    response = client.get(
        f"{settings.API_V1_STR}/active-comments/owner/ids/{owner_id}",
    )
    return response.json()


def get_active_comments_count_by_post_id(post_id: int):
    response = client.get(
        f"{settings.API_V1_STR}/active-comments/post/count/{post_id}",
    )
    return response.json()


def get_active_comments_ids_by_post_id(post_id: int):
    response = client.get(
        f"{settings.API_V1_STR}/active-comments/post/ids/{post_id}",
    )
    return response.json()


def like_post(post_id: int, token: str):
    response = client.post(
        f"{settings.API_V1_STR}/likes/post/{post_id}",
        headers=token,
    )

    return response.json()


def unlike_post(post_id: int, token: str):
    response = client.delete(
        f"{settings.API_V1_STR}/likes/post/{post_id}",
        headers=token,
    )
    return response.json()


def like_comment(comment_id: int, token: str):
    response = client.post(
        f"{settings.API_V1_STR}/likes/comment/{comment_id}",
        headers=token,
    )
    return response.json()


def unlike_comment(comment_id: int, token: str):
    response = client.delete(
        f"{settings.API_V1_STR}/likes/comment/{comment_id}",
        headers=token,
    )
    return response.json()


def get_all_active_likes_count():
    response = client.get(
        f"{settings.API_V1_STR}/active-likes/count/",
    )
    return response.json()


def active_likes_by_comment_id(comment_id: int):
    response = client.get(
        f"{settings.API_V1_STR}/likes/comment/count/{comment_id}",
    )
    return response.json()


def follow_user(following_id: int, token: str):
    response = client.post(
        f"{settings.API_V1_STR}/follows/{following_id}",
        headers=token,
    )
    return response.json()


def get_all_active_follows_count():
    response = client.get(
        f"{settings.API_V1_STR}/active-follows/count/",
    )
    return response.json()


def get_all_follows_count():
    response = client.get(
        f"{settings.API_V1_STR}/follows/count/",
    )
    return response.json()


def get_follower_count_by_user_id(user_id: int):
    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/follower/count/{user_id}",
        headers=superuser_token
    )

    return response.json()


def get_follower_ids_by_user_id(user_id: int):
    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/follower/ids/{user_id}",
        headers=superuser_token
    )

    return response.json()


def get_following_count_by_user_id(user_id: int):
    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/following/count/{user_id}",
        headers=superuser_token
    )

    return response.json()


def get_following_ids_by_user_id(user_id: int):
    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/following/ids/{user_id}",
        headers=superuser_token
    )

    return response.json()
