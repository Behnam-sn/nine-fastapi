from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import (create_random_user, deactivate_user, follow_user,
                             get_active_user, get_all_active_follows_count,
                             random_lower_string)


def test_get_all_active_follows():
    response = client.get(
        f"{settings.API_V1_STR}/active-follows/all/",
    )

    assert response.status_code == 200


def test_get_all_active_follows_is_all_active():
    # username = random_lower_string()
    # password = random_lower_string()
    # token = create_random_user(username=username, password=password)

    # second_username = random_lower_string()
    # second_password = random_lower_string()
    # create_random_user(username=second_username, password=second_password)
    # second_user = get_active_user(username=second_username)

    # follow_user(following_id=second_user["id"], token=token)

    # count = get_all_active_follows_count()
    # deactivate_user(username=username, token=token)
    # new_count = get_all_active_follows_count()

    # assert new_count == count - 1
    pass


def test_get_active_follow_by_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow = follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/{follow['id']}",
    )
    response_follow = response.json()

    assert response.status_code == 200
    assert response_follow == follow


def test_get_not_existing_follow_by_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow = follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/{follow['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_deactivated_follow_by_id():
    pass


def test_get_all_active_follows_count():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/count/",
    )
    count = response.json()

    assert response.status_code == 200
    assert count > 0


def test_get_all_active_follows_count_is_all_active():
    pass


def test_get_active_following_count_by_user_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/following/count/{user['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_active_following_count_by_user_id_is_all_active():
    pass


def test_get_active_following_count_by_not_existing_user_id():
    username = random_lower_string()
    password = random_lower_string()
    create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/following/count/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_following_count_by_deactivated_user_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/following/count/{user['id']}",
    )

    assert response.status_code == 404


def test_get_active_following_ids_by_user_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/following/ids/{user['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_active_following_ids_by_user_id_is_all_active():
    pass


def test_get_active_following_ids_by_not_existing_user_id():
    username = random_lower_string()
    password = random_lower_string()
    create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/following/ids/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_following_ids_by_deactivated_user_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/following/ids/{user['id']}",
    )

    assert response.status_code == 404


def test_get_active_follower_count_by_user_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/follower/count/{second_user['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_active_follower_count_by_user_id_is_all_active():
    pass


def test_get_active_follower_count_by_not_existing_user_id():
    username = random_lower_string()
    password = random_lower_string()
    create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/follower/count/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_follower_count_by_deactivated_user_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/follower/count/{user['id']}",
    )

    assert response.status_code == 404


def test_get_active_follower_ids_by_user_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/follower/ids/{second_user['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_active_follower_ids_by_user_id_is_all_active():
    pass


def test_get_active_follower_ids_by_not_existing_user_id():
    username = random_lower_string()
    password = random_lower_string()
    create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/follower/ids/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_follower_ids_by_deactivated_user_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-follows/follower/ids/{user['id'] + 1}",
    )

    assert response.status_code == 404
