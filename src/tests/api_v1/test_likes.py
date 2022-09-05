from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import utils


def test_like_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_post(token=token)

    response = client.post(
        f"{settings.API_V1_STR}/likes/post/{post['id']}",
        headers=token,
    )
    like = response.json()

    assert response.status_code == 200
    assert like["owner_id"] == user["id"]
    assert like["post_id"] == post["id"]


def test_liked_post_likes_count_update():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    utils.like_post(post_id=post["id"], token=token)
    updated_post = utils.get_active_post(post_id=post["id"])

    assert updated_post["likes"] == 1


def test_like_not_existing_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    response = client.post(
        f"{settings.API_V1_STR}/likes/post/{post['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_like_deactivated_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    utils.deactivate_post(post_id=post["id"], token=token)

    response = client.post(
        f"{settings.API_V1_STR}/likes/post/{post['id']}",
        headers=token,
    )

    assert response.status_code == 404


def test_like_post_already_liked():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    utils.like_post(post_id=post["id"], token=token)

    response = client.post(
        f"{settings.API_V1_STR}/likes/post/{post['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_unlike_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_post(token=token)

    utils.like_post(post_id=post["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/likes/post/{post['id']}",
        headers=token,
    )
    like = response.json()

    assert response.status_code == 200
    assert like["owner_id"] == user["id"]
    assert like["post_id"] == post["id"]


def test_unlike_not_existing_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    utils.like_post(post_id=post["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/likes/post/{post['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_unlike_deactivated_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    utils.like_post(post_id=post["id"], token=token)
    utils.deactivate_post(post_id=post["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/likes/post/{post['id']}",
        headers=token,
    )

    assert response.status_code == 404


def test_unlike_not_liked_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/likes/post/{post['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_like_comment():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    response = client.post(
        f"{settings.API_V1_STR}/likes/comment/{comment['id']}",
        headers=token,
    )
    like = response.json()

    assert response.status_code == 200
    assert like["owner_id"] == user["id"]
    assert like["comment_id"] == comment["id"]


def test_like_not_existing_comment():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    response = client.post(
        f"{settings.API_V1_STR}/likes/comment/{comment['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_like_deactivated_comment():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.deactivate_comment(comment_id=comment["id"], token=token)

    response = client.post(
        f"{settings.API_V1_STR}/likes/comment/{comment['id']}",
        headers=token,
    )

    assert response.status_code == 404


def test_like_comment_already_liked():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_comment(comment_id=comment["id"], token=token)

    response = client.post(
        f"{settings.API_V1_STR}/likes/comment/{comment['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_unlike_comment():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_comment(comment_id=comment["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/likes/comment/{comment['id']}",
        headers=token,
    )
    like = response.json()

    assert response.status_code == 200
    assert like["owner_id"] == user["id"]
    assert like["comment_id"] == comment["id"]


def test_unlike_not_existing_comment():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_comment(comment_id=comment["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/likes/comment/{comment['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_unlike_deactivated_comment():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_comment(comment_id=comment["id"], token=token)
    utils.deactivate_comment(comment_id=comment["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/likes/comment/{comment['id']}",
        headers=token,
    )

    assert response.status_code == 404


def test_unlike_not_liked_comment():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/likes/comment/{comment['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_get_all_likes_as_super_user():
    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/all/",
        headers=superuser_token,
    )

    assert response.status_code == 200


def test_get_all_likes_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/likes/all/",
        headers=token,
    )

    assert response.status_code == 401


def test_get_all_likes_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_post(post_id=post["id"], token=token)
    utils.like_comment(comment_id=comment["id"], token=token)

    count = utils.get_all_likes_count()
    utils.deactivate_user(username=username, token=token)
    new_count = utils.get_all_likes_count()

    assert new_count == count


def test_get_like_by_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    like = utils.like_post(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/{like['id']}",
        headers=superuser_token,
    )
    response_like = response.json()

    assert response.status_code == 200
    assert response_like == like


def test_get_like_by_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    like = utils.like_post(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/likes/{like['id']}",
    )

    assert response.status_code == 401


def test_get_not_existing_like_by_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    like = utils.like_post(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/{like['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


# teest_get_user_deactivated_like_by_id
# teest_get_post_deactivated_like_by_id
# teest_get_post_owner_deactivated_like_by_id
# teest_get_comment_deactivated_like_by_id
# teest_get_comment_owner_deactivated_like_by_id


def test_get_likes_count_by_owner_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_post(post_id=post["id"], token=token)
    utils.like_comment(comment_id=comment["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/owner/count/{user['id']}",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 2


def test_get_likes_count_by_owner_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/likes/owner/count/{user['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_likes_count_by_owner_id_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_post(post_id=post["id"], token=token)
    utils.like_comment(comment_id=comment["id"], token=token)

    count = utils.get_likes_count_by_owner_id(owner_id=user["id"])
    utils.deactivate_user(username=username, token=token)
    new_count = utils.get_likes_count_by_owner_id(owner_id=user["id"])

    assert new_count == count


def test_get_likes_count_by_not_existing_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/owner/count/{user['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_likes_count_by_deactivated_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_post(post_id=post["id"], token=token)
    utils.like_comment(comment_id=comment["id"], token=token)

    utils.deactivate_user(username=username, token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/owner/count/{user['id']}",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 2


def test_get_likes_ids_by_owner_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_post(post_id=post["id"], token=token)
    utils.like_comment(comment_id=comment["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/owner/ids/{user['id']}",
        headers=superuser_token,
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 2


def test_get_likes_ids_by_owner_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/likes/owner/ids/{user['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_likes_ids_by_owner_id_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_post(post_id=post["id"], token=token)
    utils.like_comment(comment_id=comment["id"], token=token)

    ids = utils.get_likes_ids_by_owner_id(owner_id=user["id"])
    utils.deactivate_user(username=username, token=token)
    new_ids = utils.get_likes_ids_by_owner_id(owner_id=user["id"])

    assert new_ids == ids


def test_get_likes_ids_by_not_existing_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/owner/ids/{user['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_likes_ids_by_deactivated_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_post(post_id=post["id"], token=token)
    utils.like_comment(comment_id=comment["id"], token=token)

    ids = utils.get_likes_ids_by_owner_id(owner_id=user["id"])
    utils.deactivate_user(username=username, token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/owner/ids/{user['id']}",
        headers=superuser_token,
    )
    response_ids = response.json()

    assert response.status_code == 200
    assert response_ids == ids


def test_get_likes_count_by_post_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    utils.like_post(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/post/count/{post['id']}",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_likes_count_by_post_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/likes/post/count/{post['id']}",
    )

    assert response.status_code == 401


def test_get_likes_count_by_post_id_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.like_post(post_id=post["id"], token=token)

    count = utils.get_likes_count_by_post_id(post_id=post["id"])
    utils.deactivate_post(post_id=post["id"], token=token)
    new_count = utils.get_likes_count_by_post_id(post_id=post["id"])

    assert new_count == count


def test_get_likes_count_by_not_existing_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/post/count/{post['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_likes_count_by_deactivated_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    utils.like_post(post_id=post["id"], token=token)
    utils.deactivate_post(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/post/count/{post['id']}",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_likes_ids_by_post_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.like_post(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/post/ids/{post['id']}",
        headers=superuser_token,
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_likes_ids_by_post_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/likes/post/ids/{post['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_likes_ids_by_post_id_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.like_post(post_id=post["id"], token=token)

    ids = utils.get_likes_ids_by_post_id(post_id=post["id"])
    utils.deactivate_post(post_id=post["id"], token=token)
    new_ids = utils.get_likes_ids_by_post_id(post_id=post["id"])

    assert new_ids == ids


def test_get_likes_ids_by_not_existing_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/post/ids/{post['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_likes_ids_by_deactivated_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.like_post(post_id=post["id"], token=token)

    ids = utils.get_likes_ids_by_post_id(post_id=post["id"])
    utils.deactivate_post(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/post/ids/{post['id']}",
        headers=superuser_token,
    )
    response_ids = response.json()

    assert response.status_code == 200
    assert response_ids == ids


def test_get_likes_count_by_comment_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_comment(comment_id=comment["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/comment/count/{comment['id']}",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_likes_count_by_comment_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/likes/comment/count/{comment['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_likes_count_by_comment_id_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)
    utils.like_comment(comment_id=comment["id"], token=token)

    count = utils.get_likes_count_by_comment_id(comment_id=comment["id"])
    utils.deactivate_comment(comment_id=comment["id"], token=token)
    new_count = utils.get_likes_count_by_comment_id(comment_id=comment["id"])

    assert new_count == count


def test_get_likes_count_by_not_existing_comment_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/comment/count/{comment['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_likes_count_by_deactivated_comment_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_comment(comment_id=comment["id"], token=token)
    utils.deactivate_comment(comment_id=comment["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/comment/count/{comment['id'] }",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_likes_ids_by_comment_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_comment(comment_id=comment["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/comment/ids/{comment['id']}",
        headers=superuser_token,
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_likes_ids_by_comment_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/likes/comment/ids/{comment['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_likes_ids_by_comment_id_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)
    utils.like_comment(comment_id=comment["id"], token=token)

    ids = utils.get_likes_ids_by_comment_id(comment_id=comment["id"])
    utils.deactivate_comment(comment_id=comment["id"], token=token)
    new_ids = utils.get_likes_ids_by_comment_id(comment_id=comment["id"])

    assert new_ids == ids


def test_get_likes_ids_by_not_existing_comment_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/comment/ids/{comment['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_likes_ids_by_deactivated_comment_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)
    utils.like_comment(comment_id=comment["id"], token=token)

    ids = utils.get_likes_ids_by_comment_id(comment_id=comment["id"])
    utils.deactivate_comment(comment_id=comment["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/likes/comment/ids/{comment['id']}",
        headers=superuser_token,
    )
    response_ids = response.json()

    assert response.status_code == 200
    assert response_ids == ids
