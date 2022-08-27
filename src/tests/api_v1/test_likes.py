from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import (authentication_headers, create_random_comment,
                             create_random_post, create_random_user,
                             deactive_comment, deactive_post, get_user,
                             like_comment, like_post, random_lower_string,
                             unlike_comment, unlike_post)


def test_get_all_likes():
    response = client.get(
        f"{settings.API_V1_STR}/likes/all/",
    )

    assert response.status_code == 200


def test_like_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_user(username=username)
    post = create_random_post(token=token)

    response = client.post(
        f"{settings.API_V1_STR}/likes/post/{post['id']}",
        headers=token,
    )
    like = response.json()

    assert response.status_code == 200
    assert like["owner_id"] == user["id"]
    assert like["post_id"] == post["id"]


def test_like_not_existing_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    response = client.post(
        f"{settings.API_V1_STR}/likes/post/{post['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_like_deactivated_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    deactive_post(id=post["id"], token=token)

    response = client.post(
        f"{settings.API_V1_STR}/likes/post/{post['id']}",
        headers=token,
    )

    assert response.status_code == 403


def test_like_post_already_liked():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    like_post(post_id=post["id"], token=token)

    response = client.post(
        f"{settings.API_V1_STR}/likes/post/{post['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_unlike_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_user(username=username)
    post = create_random_post(token=token)

    like_post(post_id=post["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/likes/post/{post['id']}",
        headers=token,
    )
    like = response.json()

    assert response.status_code == 200
    assert like["owner_id"] == user["id"]
    assert like["post_id"] == post["id"]


def test_unlike_not_existing_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    like_post(post_id=post["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/likes/post/{post['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_unlike_deactivated_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    like_post(post_id=post["id"], token=token)
    deactive_post(id=post["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/likes/post/{post['id']}",
        headers=token,
    )

    assert response.status_code == 403


def test_unlike_not_liked_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/likes/post/{post['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_like_comment():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_user(username=username)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    response = client.post(
        f"{settings.API_V1_STR}/likes/comment/{comment['id']}",
        headers=token,
    )
    like = response.json()

    assert response.status_code == 200
    assert like["owner_id"] == user["id"]
    assert like["comment_id"] == comment["id"]


def test_like_not_existing_comment():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    response = client.post(
        f"{settings.API_V1_STR}/likes/comment/{comment['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_like_deactivated_comment():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    deactive_comment(id=comment["id"], token=token)

    response = client.post(
        f"{settings.API_V1_STR}/likes/comment/{comment['id']}",
        headers=token,
    )

    assert response.status_code == 403


def test_like_comment_already_liked():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(token=token, post_id=post["id"])

    like_comment(comment_id=comment["id"], token=token)

    response = client.post(
        f"{settings.API_V1_STR}/likes/comment/{comment['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_unlike_comment():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_user(username=username)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    like_comment(comment_id=comment["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/likes/comment/{comment['id']}",
        headers=token,
    )
    like = response.json()

    assert response.status_code == 200
    assert like["owner_id"] == user["id"]
    assert like["comment_id"] == comment["id"]


def test_unlike_not_existing_comment():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    like_comment(comment_id=comment["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/likes/comment/{comment['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_unlike_deactivated_comment():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    like_comment(comment_id=comment["id"], token=token)
    deactive_comment(id=comment["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/likes/comment/{comment['id']}",
        headers=token,
    )

    assert response.status_code == 403


def test_unlike_not_liked_comment():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/likes/comment/{comment['id']}",
        headers=token,
    )

    assert response.status_code == 400


def test_get_likes_count_by_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_user(username=username)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    like_post(post_id=post["id"], token=token)
    like_comment(comment_id=comment["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/likes/owner/count/{user['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 2


def test_get_not_existing_user_likes_count_by_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    user = get_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/likes/owner/count/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_likes_ids_by_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_user(username=username)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    like_post(post_id=post["id"], token=token)
    like_comment(comment_id=comment["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/likes/owner/ids/{user['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 2


def test_get_not_existing_user_likes_ids_by_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    user = get_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/likes/owner/ids/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_likes_count_by_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    like_post(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/likes/post/count/{post['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_not_existing_post_likes_count_by_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/likes/post/count/{post['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_likes_ids_by_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    like_post(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/likes/post/ids/{post['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_not_existing_post_likes_ids_by_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/likes/post/ids/{post['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_likes_count_by_comment_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    like_comment(comment_id=comment["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/likes/comment/count/{comment['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_not_existing_comment_likes_count_by_comment_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/likes/comment/count/{comment['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_likes_ids_by_comment_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    like_comment(comment_id=comment["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/likes/comment/ids/{comment['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_not_existing_comment_likes_ids_by_comment_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/likes/comment/ids/{comment['id'] + 1}",
    )

    assert response.status_code == 404
