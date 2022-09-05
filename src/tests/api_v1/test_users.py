from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import utils


def test_update_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)

    data = {
        "username": utils.random_lower_string(),
        "name": utils.random_lower_string(),
        "bio": utils.random_lower_string()
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
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)

    random_username = utils.random_lower_string()
    random_password = utils.random_lower_string()

    token = utils.create_user(
        username=random_username, password=random_password
    )

    data = {
        "username": username,
        "name": utils.random_lower_string(),
        "bio": utils.random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/users/",
        headers=token,
        json=data,
    )

    assert response.status_code == 400


def test_update_deactivated_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    utils.deactivate_user(username=username, token=token)

    data = {
        "username": utils.random_lower_string(),
        "name": utils.random_lower_string(),
        "bio": utils.random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/users/",
        headers=token,
        json=data,
    )

    assert response.status_code == 404


# def test_activate_user_as_superuser():
#     username = utils.random_lower_string()
#     password = utils.random_lower_string()

#     utils.create_user(username=username, password=password)
#     superuser_token = authentication_headers(
#         username=settings.SUPERUSER_USERNAME,
#         password=settings.SUPERUSER_PASSWORD
#     )

#     response = client.put(
#         f"{settings.API_V1_STR}/users/activate/{username}",
#         headers=superuser_token,
#     )
#     user = response.json()

#     assert response.status_code == 200
#     assert user["is_active"] == True


# def test_activate_user_as_normal_user():
#     username = utils.random_lower_string()
#     password = utils.random_lower_string()

#     token = utils.create_user(username=username, password=password)

#     response = client.put(
#         f"{settings.API_V1_STR}/users/activate/{username}",
#         headers=token,
#     )
#     user = response.json()

#     assert response.status_code == 200
#     assert user["is_active"] == True


def test_activate_not_existing_user():
    username = utils.random_lower_string()

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.put(
        f"{settings.API_V1_STR}/users/activate/{username}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_unauthorized_activate_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)

    random_username = utils.random_lower_string()
    random_password = utils.random_lower_string()

    token = utils.create_user(
        username=random_username, password=random_password
    )

    response = client.put(
        f"{settings.API_V1_STR}/users/activate/{username}",
        headers=token,
    )

    assert response.status_code == 401


# def test_deactivate_user():
#     username = utils.random_lower_string()
#     password = utils.random_lower_string()

#     token = utils.create_user(username=username, password=password)
#     user = get_user(username=username)
#     post = create_post(token=token)
#     comment = create_comment(post_id=post["id"], token=token)

#     user_post_count = active_posts_count_by_owner_id(owner_id=user["id"])

#     utils.deactivate_user(username=username, token=token)

#     new_user_post_count = active_posts_count_by_owner_id(owner_id=user["id"])

#     assert new_user_post_count == user_post_count - 1


def test_deactivate_user_as_superuser():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)
    superuser_token = utils.authentication_headers(
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
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)

    response = client.put(
        f"{settings.API_V1_STR}/users/deactivate/{username}",
        headers=token,
    )
    user = response.json()

    assert response.status_code == 200
    assert user["is_active"] == False


def test_deactivate_not_existing_user():
    username = utils.random_lower_string()

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.put(
        f"{settings.API_V1_STR}/users/deactivate/{username}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_unauthorized_deactivate_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)

    random_username = utils.random_lower_string()
    random_password = utils.random_lower_string()

    token = utils.create_user(
        username=random_username, password=random_password
    )

    response = client.put(
        f"{settings.API_V1_STR}/users/deactivate/{username}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_current_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/users/current-user/",
        headers=token,
    )
    user = response.json()

    assert response.status_code == 200
    assert user["username"] == username


def test_get_all_users_as_superuser():
    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/users/all/",
        headers=superuser_token,
    )

    assert response.status_code == 200


def test_get_all_users_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/users/all/",
        headers=token,
    )

    assert response.status_code == 401


def test_get_all_users_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)

    all_users_count = utils.get_all_users_count()
    utils.deactivate_user(username=username, token=token)
    new_all_users_count = utils.get_all_users_count()

    assert new_all_users_count == all_users_count


def test_get_user_by_username_as_superuser():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/users/{username}",
        headers=superuser_token,
    )
    user = response.json()

    assert response.status_code == 200
    assert user["username"] == username


def test_get_user_by_username_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/users/{username}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_not_existing_user_by_username():
    username = utils.random_lower_string()

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/users/{username}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_deactivated_user_by_username():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    utils.deactivate_user(username=username, token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/users/{username}",
        headers=superuser_token,
    )
    user = response.json()

    assert response.status_code == 200
    assert user["username"] == username
    assert user["is_active"] == False


def test_get_all_users_count_as_super_user():
    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/users/count/",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count > 0


def test_get_all_users_count_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/users/count/",
        headers=token,
    )

    assert response.status_code == 401


def test_get_all_users_count_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)

    all_users_count = utils.get_all_users_count()
    utils.deactivate_user(username=username, token=token)
    new_all_users_count = utils.get_all_users_count()

    assert new_all_users_count == all_users_count
