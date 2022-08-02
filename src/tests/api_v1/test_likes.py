from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import (create_random_comment, create_random_post,
                             create_random_user, like_comment, like_post,
                             random_lower_string, unlike_comment, unlike_post,
                             user_authentication_headers)


def test_get_all_likes():
    response = client.get(
        f"{settings.API_V1_STR}/likes/",
    )

    assert response.status_code == 200


def test_like_post():
    username = random_lower_string()
    password = random_lower_string()

    user = create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    post = create_random_post(token=token)

    response = client.post(
        f"{settings.API_V1_STR}/likes/post/{post['id']}",
        headers=token,
    )
    like = response.json()

    assert response.status_code == 200
    assert like["owner_id"] == user["id"]
    assert like["post_id"] == post["id"]


def test_like_post_already_liked():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    post = create_random_post(token=token)
    like_post(token=token, post_id=post['id'])

    response = client.post(
        f"{settings.API_V1_STR}/likes/post/{post['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_unlike_post():
    username = random_lower_string()
    password = random_lower_string()

    user = create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    post = create_random_post(token=token)
    like_post(token=token, post_id=post['id'])

    response = client.delete(
        f"{settings.API_V1_STR}/likes/post/{post['id']}",
        headers=token,
    )
    like = response.json()

    assert response.status_code == 200
    assert like["owner_id"] == user["id"]
    assert like["post_id"] == post["id"]


def test_unlike_post_already_unliked():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    post = create_random_post(token=token)
    like_post(token=token, post_id=post['id'])
    unlike_post(token=token, post_id=post['id'])

    response = client.delete(
        f"{settings.API_V1_STR}/likes/post/{post['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_like_comment():
    username = random_lower_string()
    password = random_lower_string()

    user = create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(token=token, post_id=post["id"])

    response = client.post(
        f"{settings.API_V1_STR}/likes/comment/{comment['id']}",
        headers=token,
    )
    like = response.json()

    assert response.status_code == 200
    assert like["owner_id"] == user["id"]
    assert like["comment_id"] == comment["id"]


def test_like_comment_already_liked():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(token=token, post_id=post["id"])
    like_comment(token=token, comment_id=comment["id"])

    response = client.post(
        f"{settings.API_V1_STR}/likes/comment/{comment['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_unlike_comment():
    username = random_lower_string()
    password = random_lower_string()

    user = create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(token=token, post_id=post["id"])
    like_comment(token=token, comment_id=comment["id"])

    response = client.delete(
        f"{settings.API_V1_STR}/likes/comment/{comment['id']}",
        headers=token,
    )
    like = response.json()

    assert response.status_code == 200
    assert like["owner_id"] == user["id"]
    assert like["comment_id"] == comment["id"]


def test_unlike_comment_already_unliked():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(token=token, post_id=post["id"])
    like_comment(token=token, comment_id=comment["id"])
    unlike_comment(token=token, comment_id=comment["id"])

    response = client.delete(
        f"{settings.API_V1_STR}/likes/comment/{comment['id']}",
        headers=token,
    )

    assert response.status_code == 400
