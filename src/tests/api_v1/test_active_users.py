from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import (create_random_user, deactivate_user,
                             get_all_active_users_count, random_lower_string)


def test_get_all_active_users():
    response = client.get(
        f"{settings.API_V1_STR}/active-users/all/",
    )

    assert response.status_code == 200


def test_get_all_active_users_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)

    all_users_count = get_all_active_users_count()
    deactivate_user(username=username, token=token)
    new_all_users_count = get_all_active_users_count()

    assert new_all_users_count == all_users_count - 1


def test_get_active_user_by_username():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/active-users/{username}",
    )
    user = response.json()

    assert response.status_code == 200
    assert user["username"] == username
    assert user["is_active"] == True


def test_get_not_existing_user_by_username():
    username = random_lower_string()

    response = client.get(
        f"{settings.API_V1_STR}/active-users/{username}",
    )

    assert response.status_code == 404


def test_get_deactivated_user_by_username():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)

    deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-users/{username}",
    )

    assert response.status_code == 404


def test_get_all_active_users_count():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/active-users/count/",
    )
    count = response.json()

    assert response.status_code == 200
    assert count > 0
