from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import (create_random_user, deactive_user,
                             random_lower_string, user_authentication_headers)


def test_get_all_active_users():
    response = client.get(
        f"{settings.API_V1_STR}/users/all/",
    )

    assert response.status_code == 200


def test_get_current_user():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/users/current-user/",
        headers=token,
    )

    assert response.status_code == 200


def test_get_active_user_by_username():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/users/{username}",
    )
    user = response.json()

    assert response.status_code == 200
    assert user["username"] == username


def test_get_not_existing_user_by_username():
    username = random_lower_string()

    response = client.get(
        f"{settings.API_V1_STR}/users/{username}",
    )

    assert response.status_code == 404


def test_get_deactivated_user_by_username():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    deactive_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/users/{username}",
    )
    response.json()

    assert response.status_code == 403


def test_update_user():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)

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


def test_update_username_to_existing_username():
    random_username = random_lower_string()
    random_password = random_lower_string()

    create_random_user(username=random_username, password=random_password)

    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)

    data = {
        "username": random_username,
        "name": random_lower_string(),
        "bio": random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/users/",
        headers=token,
        json=data,
    )

    assert response.status_code == 400


def test_update_deactivated_user():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    deactive_user(username=username, token=token)

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

    assert response.status_code == 403


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


def test_activate_user_as_normal_user():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)

    response = client.put(
        f"{settings.API_V1_STR}/users/activate/{username}",
        headers=token,
    )
    user = response.json()

    assert response.status_code == 200
    assert user["is_active"] == True


def test_activate_not_existing_user():
    username = random_lower_string()

    superuser_token = user_authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.put(
        f"{settings.API_V1_STR}/users/activate/{username}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_unauthorized_activate_user():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)

    random_username = random_lower_string()
    random_password = random_lower_string()

    token = create_random_user(
        username=random_username, password=random_password
    )

    response = client.put(
        f"{settings.API_V1_STR}/users/activate/{username}",
        headers=token,
    )

    assert response.status_code == 401


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


def test_deactivate_user_as_normal_user():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)

    response = client.put(
        f"{settings.API_V1_STR}/users/deactivate/{username}",
        headers=token,
    )
    user = response.json()

    assert response.status_code == 200
    assert user["is_active"] == False


def test_deactivate_not_existing_user():
    username = random_lower_string()

    superuser_token = user_authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.put(
        f"{settings.API_V1_STR}/users/deactivate/{username}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_unauthorized_deactivate_user():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)

    random_username = random_lower_string()
    random_password = random_lower_string()

    token = create_random_user(
        username=random_username, password=random_password
    )

    response = client.put(
        f"{settings.API_V1_STR}/users/deactivate/{username}",
        headers=token,
    )

    assert response.status_code == 401
