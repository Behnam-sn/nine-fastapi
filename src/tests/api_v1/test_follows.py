from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import (create_random_user, follow_user,
                             random_lower_string, user_authentication_headers)


def test_get_all_follows():
    response = client.get(
        f"{settings.API_V1_STR}/follows/",
    )

    assert response.status_code == 200


def test_follow_user():
    username = random_lower_string()
    password = random_lower_string()

    user = create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    second_user = create_random_user(
        username=random_lower_string(), password=random_lower_string()
    )

    response = client.post(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )
    follow = response.json()

    assert response.status_code == 200
    assert follow["follower_id"] == user["id"]
    assert follow["following_id"] == second_user["id"]


def test_follow_not_existing_user():
    username = random_lower_string()
    password = random_lower_string()

    user = create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)

    response = client.post(
        f"{settings.API_V1_STR}/follows/{user['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_user_follow_themself():
    username = random_lower_string()
    password = random_lower_string()

    user = create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)

    response = client.post(
        f"{settings.API_V1_STR}/follows/{user['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_follow_already_followed_user():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    second_user = create_random_user(
        username=random_lower_string(), password=random_lower_string()
    )
    follow_user(token=token, following_id=second_user["id"])

    response = client.post(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_unfollow_user():
    username = random_lower_string()
    password = random_lower_string()

    user = create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    second_user = create_random_user(
        username=random_lower_string(), password=random_lower_string()
    )
    follow_user(token=token, following_id=second_user["id"])

    response = client.delete(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )
    follow = response.json()

    assert response.status_code == 200
    assert follow["follower_id"] == user["id"]
    assert follow["following_id"] == second_user["id"]


def test_unfollow_not_existing_user():
    username = random_lower_string()
    password = random_lower_string()

    user = create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)

    response = client.delete(
        f"{settings.API_V1_STR}/follows/{user['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_user_unfollow_themself():
    username = random_lower_string()
    password = random_lower_string()

    user = create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)

    response = client.delete(
        f"{settings.API_V1_STR}/follows/{user['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_unfollow_not_followed_user():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    second_user = create_random_user(
        username=random_lower_string(), password=random_lower_string()
    )

    response = client.delete(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )

    assert response.status_code == 400
