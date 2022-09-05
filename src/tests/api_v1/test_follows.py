from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import utils


def test_follow_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    response = client.post(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )
    follow = response.json()

    assert response.status_code == 200
    assert follow["follower_id"] == user["id"]
    assert follow["following_id"] == second_user["id"]


def test_user_followings_count_after_follow():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)
    user = utils.get_active_user(username=username)

    assert user["followings"] == 1


def test_user_followers_count_after_follow():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)
    updated_second_user = utils.get_active_user(username=second_username)

    assert updated_second_user["followers"] == 1


def test_follow_not_existing_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.post(
        f"{settings.API_V1_STR}/follows/{user['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_follow_deactivated_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    second_token = utils.create_user(
        username=second_username, password=second_password
    )
    second_user = utils.get_active_user(username=second_username)

    utils.deactivate_user(username=second_username, token=second_token)

    response = client.post(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )

    assert response.status_code == 404


def test_user_follow_themself():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.post(
        f"{settings.API_V1_STR}/follows/{user['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_follow_already_followed_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    response = client.post(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_unfollow_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )
    follow = response.json()

    assert response.status_code == 200
    assert follow["follower_id"] == user["id"]
    assert follow["following_id"] == second_user["id"]


def test_user_followings_count_after_unfollow():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)
    utils.unfollow_user(following_id=second_user["id"], token=token)
    user = utils.get_active_user(username=username)

    assert user["followings"] == 0


def test_user_followers_count_after_unfollow():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)
    utils.unfollow_user(following_id=second_user["id"], token=token)
    updated_second_user = utils.get_active_user(username=second_username)

    assert updated_second_user["followers"] == 0


def test_unfollow_not_existing_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.delete(
        f"{settings.API_V1_STR}/follows/{user['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_unfollow_deactivated_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    second_token = utils.create_user(
        username=second_username, password=second_password
    )
    second_user = utils.get_active_user(username=second_username)

    utils.deactivate_user(username=second_username, token=second_token)

    response = client.delete(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )

    assert response.status_code == 404


def test_user_unfollow_themself():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.delete(
        f"{settings.API_V1_STR}/follows/{user['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_unfollow_not_followed_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    response = client.delete(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_get_all_follows_as_super_user():
    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/all/",
        headers=superuser_token,
    )

    assert response.status_code == 200


def test_get_all_follows_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/follows/all/",
        headers=token,
    )

    assert response.status_code == 401


def test_get_all_follows_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    count = utils.get_all_follows_count()
    utils.deactivate_user(username=username, token=token)
    new_count = utils.get_all_follows_count()

    assert new_count == count


def test_get_follow_by_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    follow = utils.follow_user(following_id=second_user["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/{follow['id']}",
        headers=superuser_token,
    )
    response_follow = response.json()

    assert response.status_code == 200
    assert response_follow == follow


def test_get_follow_by_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    follow = utils.follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/follows/{follow['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_not_existing_follow_by_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    follow = utils.follow_user(following_id=second_user["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/{follow['id'] + 1}",
        headers=superuser_token,
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

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/{follow['id']}",
        headers=superuser_token,
    )
    response_follow = response.json()

    assert response.status_code == 200
    assert response_follow["id"] == follow["id"]
    assert response_follow["is_follower_active"] == False


def test_get_all_followers_count_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/count/",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count > 0


def test_get_all_followers_count_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/follows/count/",
        headers=token,
    )

    assert response.status_code == 401


def test_get_all_followers_count_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    count = utils.get_all_follows_count()
    utils.deactivate_user(username=username, token=token)
    new_count = utils.get_all_follows_count()

    assert new_count == count


def test_get_follower_count_by_user_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/follower/count/{second_user['id']}",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_follower_count_by_user_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/follows/follower/count/{user['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_follower_count_by_user_id_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    count = utils.get_follower_count_by_user_id(user_id=second_user["id"])
    utils.deactivate_user(username=username, token=token)
    new_count = utils.get_follower_count_by_user_id(user_id=second_user["id"])

    assert new_count == count


def test_get_follower_count_by_not_existing_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/follower/count/{user['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_follower_count_by_deactivated_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)
    utils.deactivate_user(username=username, token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/follower/count/{second_user['id']}",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_follower_ids_by_user_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/follower/ids/{second_user['id']}",
        headers=superuser_token,
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_follower_ids_by_user_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/follows/follower/ids/{user['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_follower_ids_by_user_id_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    ids = utils.get_follower_ids_by_user_id(user_id=second_user["id"])
    utils.deactivate_user(username=username, token=token)
    new_ids = utils.get_follower_ids_by_user_id(user_id=second_user["id"])

    assert new_ids == ids


def test_get_follower_ids_by_not_existing_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/follower/ids/{user['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_follower_ids_by_deactivated_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    ids = utils.get_follower_ids_by_user_id(user_id=user["id"])
    utils.deactivate_user(username=username, token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/follower/ids/{user['id']}",
        headers=superuser_token,
    )
    response_ids = response.json()

    assert response.status_code == 200
    assert response_ids == ids


def test_get_following_count_by_user_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/following/count/{user['id']}",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_following_count_by_user_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/follows/following/count/{user['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_following_count_by_user_id_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    count = utils.get_following_count_by_user_id(user_id=user["id"])
    utils.deactivate_user(username=second_username, token=token)
    new_count = utils.get_following_count_by_user_id(user_id=user["id"])

    assert new_count == count


def test_get_following_count_by_not_existing_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/following/count/{user['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_following_count_by_deactivated_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)
    utils.deactivate_user(username=username, token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/following/count/{user['id']}",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_following_ids_by_user_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/following/ids/{user['id']}",
        headers=superuser_token,
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_following_ids_by_user_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/follows/following/ids/{user['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_following_ids_by_user_id_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    ids = utils.get_following_ids_by_user_id(user_id=second_user["id"])
    utils.deactivate_user(username=second_username, token=token)
    new_ids = utils.get_following_ids_by_user_id(user_id=second_user["id"])

    assert new_ids == ids


def test_get_following_ids_by_not_existing_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/following/ids/{user['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_following_ids_by_deactivated_user_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    second_username = utils.random_lower_string()
    second_password = utils.random_lower_string()
    utils.create_user(username=second_username, password=second_password)
    second_user = utils.get_active_user(username=second_username)

    utils.follow_user(following_id=second_user["id"], token=token)

    ids = utils.get_following_ids_by_user_id(user_id=user["id"])
    utils.deactivate_user(username=username, token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/following/ids/{user['id']}",
        headers=superuser_token,
    )
    response_ids = response.json()

    assert response.status_code == 200
    assert response_ids == ids
