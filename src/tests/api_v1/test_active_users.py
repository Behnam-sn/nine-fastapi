from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import utils


def test_get_all_active_users():
    response = client.get(
        f"{settings.API_V1_STR}/active-users/all/",
    )

    assert response.status_code == 200


def test_get_all_active_users_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)

    count = utils.get_all_active_users_count()
    utils.deactivate_user(username=username, token=token)
    new_count = utils.get_all_active_users_count()

    assert new_count == count - 1


def test_get_active_user_by_username():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/active-users/{username}",
    )
    user = response.json()

    assert response.status_code == 200
    assert user["username"] == username
    assert user["is_active"] == True


def test_get_not_existing_user_by_username():
    username = utils.random_lower_string()

    response = client.get(
        f"{settings.API_V1_STR}/active-users/{username}",
    )

    assert response.status_code == 404


def test_get_deactivated_user_by_username():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    utils.deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-users/{username}",
    )

    assert response.status_code == 404


def test_get_all_active_users_count():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/active-users/count/",
    )
    count = response.json()

    assert response.status_code == 200
    assert count > 0


def test_get_all_active_users_count_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)

    count = utils.get_all_active_users_count()
    utils.deactivate_user(username=username, token=token)
    new_count = utils.get_all_active_users_count()

    assert new_count == count - 1
