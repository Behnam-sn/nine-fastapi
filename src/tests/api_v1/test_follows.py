from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import (create_random_user, deactive_user, follow_user,
                             get_user, random_lower_string)


def test_get_all_follows():
    response = client.get(
        f"{settings.API_V1_STR}/follows/all/",
    )

    assert response.status_code == 200


def test_follow_user():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_user(username=username)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_user(username=second_username)

    response = client.post(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )
    follow = response.json()

    assert response.status_code == 200
    assert follow["follower_id"] == user["id"]
    assert follow["following_id"] == second_user["id"]


def test_follow_not_existing_user():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_user(username=username)

    response = client.post(
        f"{settings.API_V1_STR}/follows/{user['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_follow_deactivated_user():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    second_token = create_random_user(
        username=second_username, password=second_password
    )
    second_user = get_user(username=second_username)

    deactive_user(username=second_username, token=second_token)

    response = client.post(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )

    assert response.status_code == 403


def test_user_follow_themself():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_user(username=username)

    response = client.post(
        f"{settings.API_V1_STR}/follows/{user['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_follow_already_followed_user():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    response = client.post(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_unfollow_user():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_user(username=username)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )
    follow = response.json()

    assert response.status_code == 200
    assert follow["follower_id"] == user["id"]
    assert follow["following_id"] == second_user["id"]


def test_unfollow_not_existing_user():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_user(username=username)

    response = client.delete(
        f"{settings.API_V1_STR}/follows/{user['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_unfollow_deactivated_user():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    second_token = create_random_user(
        username=second_username, password=second_password
    )
    second_user = get_user(username=second_username)

    deactive_user(username=second_username, token=second_token)

    response = client.delete(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )

    assert response.status_code == 403


def test_user_unfollow_themself():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_user(username=username)

    response = client.delete(
        f"{settings.API_V1_STR}/follows/{user['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_unfollow_not_followed_user():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(
        username=second_username, password=second_password
    )
    second_user = get_user(username=second_username)

    response = client.delete(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_get_follow_by_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_user(username=second_username)

    follow = follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/follows/{follow['id']}",
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
    second_user = get_user(username=second_username)

    follow = follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/follows/{follow['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_follower_count_by_user_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/follows/follower/count/{second_user['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_not_existing_user_follower_count_by_user_id():
    username = random_lower_string()
    password = random_lower_string()
    create_random_user(username=username, password=password)
    user = get_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/follows/follower/count/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_follower_ids_by_user_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/follows/follower/ids/{second_user['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_not_existing_user_follower_ids_by_user_id():
    username = random_lower_string()
    password = random_lower_string()
    create_random_user(username=username, password=password)
    user = get_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/follows/follower/ids/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_following_count_by_user_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_user(username=username)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/follows/following/count/{user['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_not_existing_user_following_count_by_user_id():
    username = random_lower_string()
    password = random_lower_string()
    create_random_user(username=username, password=password)
    user = get_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/follows/following/count/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_following_ids_by_user_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_user(username=username)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/follows/following/ids/{user['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_not_existing_user_following_ids_by_user_id():
    username = random_lower_string()
    password = random_lower_string()
    create_random_user(username=username, password=password)
    user = get_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/follows/following/ids/{user['id'] + 1}",
    )

    assert response.status_code == 404
