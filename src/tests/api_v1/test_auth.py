from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import (create_random_user, random_lower_string,
                             user_authentication_headers)


def test_signup():
    data = {
        "username": random_lower_string(),
        "name": random_lower_string(),
        "password": random_lower_string()
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json=data
    )

    assert response.status_code == 200


def test_signup_with_existing_username():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)

    data = {
        "username": username,
        "name": random_lower_string(),
        "password": random_lower_string()
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json=data
    )

    assert response.status_code == 400


def test_login():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)

    data = {
        "username": username,
        "password": password
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=data
    )
    tokens = response.json()

    assert response.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_login_as_superuser():
    data = {
        "username": settings.SUPERUSER_USERNAME,
        "password": settings.SUPERUSER_PASSWORD
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=data
    )

    assert response.status_code == 200


def test_login_with_wrong_password():
    username = random_lower_string()

    create_random_user(username=username, password=random_lower_string())

    data = {
        "username": username,
        "password": random_lower_string()
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=data
    )

    assert response.status_code == 401


def test_test_token():
    username = random_lower_string()
    password = random_lower_string()

    random_user = create_random_user(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)

    response = client.post(
        f"{settings.API_V1_STR}/auth/test-token",
        headers=token,
    )
    user = response.json()

    assert response.status_code == 200
    assert user == random_user
