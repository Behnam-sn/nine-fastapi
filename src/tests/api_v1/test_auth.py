from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import utils


def test_signup():
    data = {
        "username": utils.random_lower_string(),
        "name": utils.random_lower_string(),
        "password": utils.random_lower_string()
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json=data
    )

    assert response.status_code == 200


def test_signup_with_existing_username():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)

    data = {
        "username": username,
        "name": utils.random_lower_string(),
        "password": utils.random_lower_string()
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json=data
    )

    assert response.status_code == 400


def test_signin():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)

    data = {
        "username": username,
        "password": password
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/signin",
        data=data
    )
    token = response.json()

    assert response.status_code == 200
    assert "access_token" in token
    assert token["access_token"]


def test_signin_as_superuser():
    data = {
        "username": settings.SUPERUSER_USERNAME,
        "password": settings.SUPERUSER_PASSWORD
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/signin",
        data=data
    )

    assert response.status_code == 200


def test_signin_with_wrong_password():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)

    data = {
        "username": username,
        "password": utils.random_lower_string()
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/signin",
        data=data
    )

    assert response.status_code == 401
