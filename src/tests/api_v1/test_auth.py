from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import create_random_user, random_lower_string


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
