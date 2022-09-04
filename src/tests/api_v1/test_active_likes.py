from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import (create_random_comment, create_random_post,
                             create_random_user, deactivate_comment,
                             deactivate_post, deactivate_user, get_active_user,
                             get_all_active_likes_count, like_comment,
                             like_post, random_lower_string)


def test_get_all_active_likes():
    response = client.get(
        f"{settings.API_V1_STR}/active-likes/all/",
    )

    assert response.status_code == 200


def test_get_all_active_likes_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    like_post(post_id=post["id"], token=token)
    like_comment(comment_id=comment["id"], token=token)

    count = get_all_active_likes_count()
    deactivate_user(username=username, token=token)
    new_count = get_all_active_likes_count()

    assert new_count == count - 2


def test_get_active_like_by_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    like = like_post(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/{like['id']}",
    )
    response_like = response.json()

    assert response.status_code == 200
    assert response_like == like


def test_get_not_existing_like_by_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    like = like_post(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/{like['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_deactivated_like_by_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    like = like_post(post_id=post["id"], token=token)
    deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/{like['id']}",
    )

    assert response.status_code == 404


def test_get_all_active_likes_count():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    like_post(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/count/",
    )
    count = response.json()

    assert response.status_code == 200
    assert count > 0


def test_get_all_active_likes_count_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    like_post(post_id=post["id"], token=token)
    like_comment(comment_id=comment["id"], token=token)

    count = get_all_active_likes_count()
    deactivate_user(username=username, token=token)
    new_count = get_all_active_likes_count()

    assert new_count == count - 2


def test_get_active_likes_count_by_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    like_post(post_id=post["id"], token=token)
    like_comment(comment_id=comment["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/owner/count/{user['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 2


def test_get_active_likes_count_by_owner_id_is_all_active():
    pass


def test_get_active_likes_count_by_not_existing_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/owner/count/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_likes_count_by_deactivated_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)
    deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/owner/count/{user['id']}",
    )

    assert response.status_code == 404


def test_get_active_likes_ids_by_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    like_post(post_id=post["id"], token=token)
    like_comment(comment_id=comment["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/owner/ids/{user['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 2


# def test_get_active_likes_ids_by_owner_id_is_all_active():
#     pass


def test_get_active_likes_ids_by_not_existing_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/owner/ids/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_likes_ids_by_deactivated_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)
    deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/owner/ids/{user['id']}",
    )

    assert response.status_code == 404


def test_get_active_likes_count_by_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    like_post(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/post/count/{post['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


# def test_get_active_likes_count_by_post_id_is_all_active():
#     pass


def test_get_active_likes_count_by_not_existing_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/post/count/{post['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_likes_count_by_deactivated_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    deactivate_post(post_id=post['id'], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/post/count/{post['id']}",
    )

    assert response.status_code == 404


def test_get_active_likes_ids_by_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    like_post(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/post/ids/{post['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


# def test_get_active_likes_ids_by_post_id_is_all_active():
#     pass


def test_get_active_likes_ids_by_not_existing_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/post/ids/{post['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_likes_ids_by_deactivated_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    deactivate_post(post_id=post['id'], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/post/ids/{post['id']}",
    )

    assert response.status_code == 404


def test_get_active_likes_count_by_comment_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    like_comment(comment_id=comment["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/comment/count/{comment['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


# def test_get_active_likes_count_by_comment_id_is_all_active():
#     pass


def test_get_active_likes_count_by_not_existing_comment_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/comment/count/{comment['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_likes_count_by_deactivated_comment_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)
    deactivate_comment(comment_id=comment["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/comment/count/{comment['id']}",
    )

    assert response.status_code == 404


def test_get_active_likes_ids_by_comment_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    like_comment(comment_id=comment["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/comment/ids/{comment['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


# def test_get_active_likes_ids_by_comment_id_is_all_active():
#     pass


def test_get_active_likes_ids_by_not_existing_comment_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/comment/ids/{comment['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_likes_ids_by_deactivated_comment_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)
    deactivate_comment(comment_id=comment["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-likes/comment/ids/{comment['id']}",
    )

    assert response.status_code == 404
