from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import (create_random_comment, create_random_post,
                             create_random_user, random_lower_string,
                             user_authentication_headers)


def test_create_comment():
    username = random_lower_string()
    password = random_lower_string()

    user = create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    post = create_random_post(token=token)

    data = {
        "text": random_lower_string(),
        "post_id": post["id"]
    }

    response = client.post(
        f"{settings.API_V1_STR}/comments/",
        headers=token,
        json=data
    )
    comment = response.json()

    assert response.status_code == 200
    assert comment["text"] == data["text"]
    assert comment["owner_id"] == user["id"]
    assert comment["post_id"] == post["id"]


def test_get_all_comments():
    response = client.get(
        f"{settings.API_V1_STR}/comments/",
    )

    assert response.status_code == 200


def test_get_comment_by_id():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    post = create_random_post(token=token)
    random_comment = create_random_comment(token=token, post_id=post["id"])

    response = client.get(
        f"{settings.API_V1_STR}/comments/{random_comment['id']}",
    )
    comment = response.json()

    assert response.status_code == 200
    assert random_comment == comment


def test_comment_on_not_existing_post():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    post = create_random_post(token=token)

    data = {
        "text": random_lower_string(),
        "post_id": post["id"] + 1
    }

    response = client.post(
        f"{settings.API_V1_STR}/comments/",
        headers=token,
        json=data
    )

    assert response.status_code == 404


def test_update_comment():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    post = create_random_post(token=token)
    random_comment = create_random_comment(token=token, post_id=post["id"])

    data = {
        "text": random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/comments/{random_comment['id']}",
        headers=token,
        json=data
    )
    comment = response.json()

    assert response.status_code == 200
    assert comment["id"] == random_comment["id"]
    assert comment["is_modified"] == True
    assert comment["text"] == data["text"]


def test_activate_comment():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    post = create_random_post(token=token)
    random_comment = create_random_comment(token=token, post_id=post["id"])

    response = client.put(
        f"{settings.API_V1_STR}/comments/activate/{random_comment['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_activate_comment_as_superuser():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    post = create_random_post(token=token)
    random_comment = create_random_comment(token=token, post_id=post["id"])

    superuser_token = user_authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.put(
        f"{settings.API_V1_STR}/comments/activate/{random_comment['id']}",
        headers=superuser_token,
    )
    comment = response.json()

    assert response.status_code == 200
    assert comment["is_active"] == True


def test_deactivate_comment():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    post = create_random_post(token=token)
    random_comment = create_random_comment(token=token, post_id=post["id"])

    response = client.put(
        f"{settings.API_V1_STR}/comments/deactivate/{random_comment['id']}",
        headers=token,
    )
    comment = response.json()

    assert response.status_code == 200
    assert comment["is_active"] == False


def test_deactivate_comment_as_superuser():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    post = create_random_post(token=token)
    random_comment = create_random_comment(token=token, post_id=post["id"])

    superuser_token = user_authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.put(
        f"{settings.API_V1_STR}/comments/deactivate/{random_comment['id']}",
        headers=superuser_token,
    )
    comment = response.json()

    assert response.status_code == 200
    assert comment["is_active"] == False


def test_delete_comment():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    post = create_random_post(token=token)
    random_comment = create_random_comment(token=token, post_id=post["id"])

    response = client.delete(
        f"{settings.API_V1_STR}/comments/{random_comment['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_delete_comment_as_superuser():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    post = create_random_post(token=token)
    random_comment = create_random_comment(token=token, post_id=post["id"])

    superuser_token = user_authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.delete(
        f"{settings.API_V1_STR}/comments/{random_comment['id']}",
        headers=superuser_token,
    )
    comment = response.json()

    assert response.status_code == 200
    assert comment == random_comment
