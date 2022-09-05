from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import utils


def test_get_all_active_follows():
    response = client.get(
        f"{settings.API_V1_STR}/active-follows/all/",
    )

    assert response.status_code == 200


def test_get_all_active_follows_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    count = utils.get_all_active_follows_count()
    utils.deactivate_user(username=username, token=token)
    new_count = utils.get_all_active_follows_count()

    assert new_count == count - 1


def test_get_active_follow_by_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    follow = utils.follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/{follow['id']}",
    )
    response_follow = response.json()

    assert response.status_code == 200
    assert response_follow == follow


def test_get_not_existing_follow_by_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    follow = utils.follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/{follow['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_deactivated_follow_by_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    follow = utils.follow_user(following_id=second_user["id"], token=token)
    utils.deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/{follow['id']}",
    )

    assert response.status_code == 404


def test_get_all_active_follows_count():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/count/",
    )
    count = response.json()

    assert response.status_code == 200
    assert count > 0


def test_get_all_active_follows_count_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    count = utils.get_all_active_follows_count()
    utils.deactivate_user(username=username, token=token)
    new_count = utils.get_all_active_follows_count()

    assert new_count == count - 1


def test_get_active_following_count_by_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/following/count/{user['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_active_following_count_by_user_id_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    second_token = utils.create_user(
        username=second_username, password=second_password
    )
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    count = utils.get_active_following_count_by_user_id(user_id=user["id"])
    utils.deactivate_user(username=second_username, token=second_token)
    new_count = utils.get_active_following_count_by_user_id(user_id=user["id"])

    assert count == 1
    assert new_count == 0


def test_get_active_following_count_by_not_existing_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/following/count/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_following_count_by_deactivated_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    utils.deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/following/count/{user['id']}",
    )

    assert response.status_code == 404


def test_get_active_following_ids_by_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/following/ids/{user['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_active_following_ids_by_user_id_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    second_token = utils.create_user(
        username=second_username, password=second_password
    )
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    ids = utils.get_active_following_ids_by_user_id(user_id=user["id"])
    utils.deactivate_user(username=second_username, token=second_token)
    new_ids = utils.get_active_following_ids_by_user_id(user_id=user["id"])

    assert len(ids) == 1
    assert len(new_ids) == 0


def test_get_active_following_ids_by_not_existing_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/following/ids/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_following_ids_by_deactivated_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    utils.deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/following/ids/{user['id']}",
    )

    assert response.status_code == 404


def test_get_active_follower_count_by_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/follower/count/{second_user['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_active_follower_count_by_user_id_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    count = utils.get_active_follower_count_by_user_id(
        user_id=second_user["id"]
    )
    utils.deactivate_user(username=username, token=token)
    new_count = utils.get_active_follower_count_by_user_id(
        user_id=second_user["id"]
    )

    assert count == 1
    assert new_count == 0


def test_get_active_follower_count_by_not_existing_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/follower/count/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_follower_count_by_deactivated_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    utils.deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/follower/count/{user['id']}",
    )

    assert response.status_code == 404


def test_get_active_follower_ids_by_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/follower/ids/{second_user['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_active_follower_ids_by_user_id_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(
        username=second_username, password=second_password
    )
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    ids = utils.get_active_follower_ids_by_user_id(user_id=second_user["id"])
    utils.deactivate_user(username=username, token=token)
    new_ids = utils.get_active_follower_ids_by_user_id(
        user_id=second_user["id"]
    )

    assert len(ids) == 1
    assert len(new_ids) == 0


def test_get_active_follower_ids_by_not_existing_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/follower/ids/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_follower_ids_by_deactivated_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    utils.deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/follower/ids/{user['id'] + 1}",
    )

    assert response.status_code == 404
