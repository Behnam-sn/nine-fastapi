from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import (create_random_user, random_lower_string,
                             user_authentication_headers)


def test_get_current_user():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/users/current-user",
        headers=token,
    )

    assert response.status_code == 200


def test_get_user_by_id():
    random_user = create_random_user()

    response = client.get(
        f"{settings.API_V1_STR}/users/id/{random_user['id']}",
    )
    user = response.json()

    assert response.status_code == 200
    assert user == random_user


def test_get_user_by_username():
    username = random_lower_string()
    random_user = create_random_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/users/username/{username}",
    )
    user = response.json()

    assert response.status_code == 200
    assert user == random_user


def test_get_all_users():
    response = client.get(
        f"{settings.API_V1_STR}/users/all",
    )

    assert response.status_code == 200


def test_update_user():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)

    data = {
        "username": random_lower_string(),
        "name": random_lower_string(),
        "bio": random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/users/",
        headers=token,
        json=data,
    )
    user = response.json()

    assert response.status_code == 200
    assert user["username"] == data["username"]
    assert user["name"] == data["name"]
    assert user["bio"] == data["bio"]


def test_activate_user():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)

    response = client.put(
        f"{settings.API_V1_STR}/users/activate/{username}",
        headers=token,
    )
    user = response.json()

    assert response.status_code == 200
    assert user["is_active"] == True


def test_activate_user_as_superuser():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    superuser_token = user_authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.put(
        f"{settings.API_V1_STR}/users/activate/{username}",
        headers=superuser_token,
    )
    user = response.json()

    assert response.status_code == 200
    assert user["is_active"] == True


def test_deactivate_user():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)

    response = client.put(
        f"{settings.API_V1_STR}/users/deactivate/{username}",
        headers=token,
    )
    user = response.json()

    assert response.status_code == 200
    assert user["is_active"] == False


def test_deactivate_user_as_superuser():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    superuser_token = user_authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.put(
        f"{settings.API_V1_STR}/users/deactivate/{username}",
        headers=superuser_token,
    )
    user = response.json()

    assert response.status_code == 200
    assert user["is_active"] == False
