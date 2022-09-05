from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import utils


def test_get_all_active_likes():
    response = client.get(
        f"{settings.API_V1_STR}/active-likes/all/",
    )

    assert response.status_code == 200


def test_get_all_active_likes_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_post(post_id=post["id"], token=token)
    utils.like_comment(comment_id=comment["id"], token=token)

    count = utils.get_all_active_likes_count()
    utils.deactivate_user(username=username, token=token)
    new_count = utils.get_all_active_likes_count()

    assert new_count == count - 2


def test_get_active_like_by_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    like = utils.like_post(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/{like['id']}",
    )
    response_like = response.json()

    assert response.status_code == 200
    assert response_like == like


def test_get_not_existing_like_by_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    like = utils.like_post(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/{like['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_deactivated_like_by_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    like = utils.like_post(post_id=post["id"], token=token)
    utils.deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/{like['id']}",
    )

    assert response.status_code == 404


def test_get_all_active_likes_count():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    utils.like_post(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/count/",
    )
    count = response.json()

    assert response.status_code == 200
    assert count > 0


def test_get_all_active_likes_count_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_post(post_id=post["id"], token=token)
    utils.like_comment(comment_id=comment["id"], token=token)

    count = utils.get_all_active_likes_count()
    utils.deactivate_user(username=username, token=token)
    new_count = utils.get_all_active_likes_count()

    assert new_count == count - 2


def test_get_active_likes_count_by_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_post(post_id=post["id"], token=token)
    utils.like_comment(comment_id=comment["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/owner/count/{user['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 2


def test_get_active_likes_count_by_owner_id_is_all_active():
    pass


def test_get_active_likes_count_by_not_existing_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/owner/count/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_likes_count_by_deactivated_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    utils.deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/owner/count/{user['id']}",
    )

    assert response.status_code == 404


def test_get_active_likes_ids_by_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_post(post_id=post["id"], token=token)
    utils.like_comment(comment_id=comment["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/owner/ids/{user['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 2


# def test_get_active_likes_ids_by_owner_id_is_all_active():
#     pass


def test_get_active_likes_ids_by_not_existing_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/owner/ids/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_likes_ids_by_deactivated_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    utils.deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/owner/ids/{user['id']}",
    )

    assert response.status_code == 404


def test_get_active_likes_count_by_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    utils.like_post(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/post/count/{post['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


# def test_get_active_likes_count_by_post_id_is_all_active():
#     pass


def test_get_active_likes_count_by_not_existing_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/post/count/{post['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_likes_count_by_deactivated_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.deactivate_post(post_id=post['id'], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/post/count/{post['id']}",
    )

    assert response.status_code == 404


def test_get_active_likes_ids_by_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    utils.like_post(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/post/ids/{post['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


# def test_get_active_likes_ids_by_post_id_is_all_active():
#     pass


def test_get_active_likes_ids_by_not_existing_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/post/ids/{post['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_likes_ids_by_deactivated_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.deactivate_post(post_id=post['id'], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/post/ids/{post['id']}",
    )

    assert response.status_code == 404


def test_get_active_likes_count_by_comment_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_comment(comment_id=comment["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/comment/count/{comment['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


# def test_get_active_likes_count_by_comment_id_is_all_active():
#     pass


def test_get_active_likes_count_by_not_existing_comment_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/comment/count/{comment['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_likes_count_by_deactivated_comment_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)
    utils.deactivate_comment(comment_id=comment["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/comment/count/{comment['id']}",
    )

    assert response.status_code == 404


def test_get_active_likes_ids_by_comment_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.like_comment(comment_id=comment["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/comment/ids/{comment['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


# def test_get_active_likes_ids_by_comment_id_is_all_active():
#     pass


def test_get_active_likes_ids_by_not_existing_comment_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/comment/ids/{comment['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_likes_ids_by_deactivated_comment_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)
    utils.deactivate_comment(comment_id=comment["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/comment/ids/{comment['id']}",
    )

    assert response.status_code == 404
