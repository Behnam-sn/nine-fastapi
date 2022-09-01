from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import (authentication_headers, create_random_user,
                             deactivate_user, follow_user, get_active_user,
                             get_all_follows_count,
                             get_follower_count_by_user_id,
                             get_follower_ids_by_user_id,
                             get_following_count_by_user_id,
                             get_following_ids_by_user_id, random_lower_string)


def test_follow_user():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

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
    user = get_active_user(username=username)

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
    second_user = get_active_user(username=second_username)

    deactivate_user(username=second_username, token=second_token)

    response = client.post(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )

    assert response.status_code == 404


def test_user_follow_themself():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

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
    second_user = get_active_user(username=second_username)

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
    user = get_active_user(username=username)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

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
    user = get_active_user(username=username)

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
    second_user = get_active_user(username=second_username)

    deactivate_user(username=second_username, token=second_token)

    response = client.delete(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )

    assert response.status_code == 404


def test_user_unfollow_themself():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

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
    second_user = get_active_user(username=second_username)

    response = client.delete(
        f"{settings.API_V1_STR}/follows/{second_user['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_get_all_follows_as_super_user():
    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/all/",
        headers=superuser_token,
    )

    assert response.status_code == 200


def test_get_all_follows_as_normal_user():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/follows/all/",
        headers=token,
    )

    assert response.status_code == 401


def test_get_all_follows_is_all():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    count = get_all_follows_count()
    deactivate_user(username=username, token=token)
    new_count = get_all_follows_count()

    assert new_count == count


def test_get_follow_by_id_as_super_user():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow = follow_user(following_id=second_user["id"], token=token)

    superuser_token = authentication_headers(
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
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow = follow_user(following_id=second_user["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/follows/{follow['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_not_existing_follow_by_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow = follow_user(following_id=second_user["id"], token=token)

    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/{follow['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_deactivated_follow_by_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow = follow_user(following_id=second_user["id"], token=token)
    deactivate_user(username=username, token=token)

    superuser_token = authentication_headers(
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
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    superuser_token = authentication_headers(
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
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/follows/count/",
        headers=token,
    )

    assert response.status_code == 401


def test_get_all_followers_count_is_all():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    count = get_all_follows_count()
    deactivate_user(username=username, token=token)
    new_count = get_all_follows_count()

    assert new_count == count


def test_get_follower_count_by_user_id_as_super_user():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    superuser_token = authentication_headers(
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
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/follows/follower/count/{user['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_follower_count_by_user_id_is_all():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    count = get_follower_count_by_user_id(user_id=second_user["id"])
    deactivate_user(username=username, token=token)
    new_count = get_follower_count_by_user_id(user_id=second_user["id"])

    assert new_count == count


def test_get_follower_count_by_not_existing_user_id():
    username = random_lower_string()
    password = random_lower_string()
    create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/follower/count/{user['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_follower_count_by_deactivated_user_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)
    deactivate_user(username=username, token=token)

    superuser_token = authentication_headers(
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
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    superuser_token = authentication_headers(
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
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/follows/follower/ids/{user['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_follower_ids_by_user_id_is_all():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    ids = get_follower_ids_by_user_id(user_id=second_user["id"])
    deactivate_user(username=username, token=token)
    new_ids = get_follower_ids_by_user_id(user_id=second_user["id"])

    assert new_ids == ids


def test_get_follower_ids_by_not_existing_user_id():
    username = random_lower_string()
    password = random_lower_string()
    create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/follower/ids/{user['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_follower_ids_by_deactivated_user_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    ids = get_follower_ids_by_user_id(user_id=user["id"])
    deactivate_user(username=username, token=token)

    superuser_token = authentication_headers(
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
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    superuser_token = authentication_headers(
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
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/follows/following/count/{user['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_following_count_by_user_id_is_all():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    count = get_following_count_by_user_id(user_id=user["id"])
    deactivate_user(username=second_username, token=token)
    new_count = get_following_count_by_user_id(user_id=user["id"])

    assert new_count == count


def test_get_following_count_by_not_existing_user_id():
    username = random_lower_string()
    password = random_lower_string()
    create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/following/count/{user['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_following_count_by_deactivated_user_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)
    deactivate_user(username=username, token=token)

    superuser_token = authentication_headers(
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
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    superuser_token = authentication_headers(
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
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/follows/following/ids/{user['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_following_ids_by_user_id_is_all():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    ids = get_following_ids_by_user_id(user_id=second_user["id"])
    deactivate_user(username=second_username, token=token)
    new_ids = get_following_ids_by_user_id(user_id=second_user["id"])

    assert new_ids == ids


def test_get_following_ids_by_not_existing_user_id():
    username = random_lower_string()
    password = random_lower_string()
    create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/follows/following/ids/{user['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_following_ids_by_deactivated_user_id():
    username = random_lower_string()
    password = random_lower_string()
    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    second_username = random_lower_string()
    second_password = random_lower_string()
    create_random_user(username=second_username, password=second_password)
    second_user = get_active_user(username=second_username)

    follow_user(following_id=second_user["id"], token=token)

    ids = get_following_ids_by_user_id(user_id=user["id"])
    deactivate_user(username=username, token=token)

    superuser_token = authentication_headers(
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
