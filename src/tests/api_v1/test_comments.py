from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import (active_comments_count_by_owner_id,
                             active_comments_count_by_post_id,
                             active_comments_ids_by_owner_id,
                             active_comments_ids_by_post_id,
                             active_likes_by_comment_id,
                             all_active_comments_count,
                             all_active_comments_ids, authentication_headers,
                             create_random_comment, create_random_post,
                             create_random_user, deactivate_comment,
                             deactivate_post, get_active_user, get_post,
                             like_comment, random_lower_string)


def test_create_comment():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)
    post = create_random_post(token=token)

    data = {
        "text": random_lower_string(),
        "post_id": post["id"]
    }

    response = client.post(
        f"{settings.API_V1_STR}/comments/",
        headers=token,
        json=data
    )
    comment = response.json()

    assert response.status_code == 200
    assert comment["text"] == data["text"]
    assert comment["owner_id"] == user["id"]
    assert comment["post_id"] == post["id"]


def test_comment_on_not_existing_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    data = {
        "text": random_lower_string(),
        "post_id": post["id"] + 1
    }

    response = client.post(
        f"{settings.API_V1_STR}/comments/",
        headers=token,
        json=data
    )

    assert response.status_code == 404


def test_comment_on_deactivated_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    deactivate_post(id=post["id"], token=token)

    data = {
        "text": random_lower_string(),
        "post_id": post["id"]
    }

    response = client.post(
        f"{settings.API_V1_STR}/comments/",
        headers=token,
        json=data
    )

    assert response.status_code == 404


def test_get_all_active_comments():
    response = client.get(
        f"{settings.API_V1_STR}/comments/all/",
    )

    assert response.status_code == 200


def test_get_active_comment_by_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    random_comment = create_random_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/comments/{random_comment['id']}",
    )
    comment = response.json()

    assert response.status_code == 200
    assert random_comment == comment


def test_get_not_existing_comment_by_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/comments/{comment['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_deactivated_comment_by_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    deactivate_comment(id=comment["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/comments/{comment['id']}",
    )

    assert response.status_code == 404


def test_update_comment():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    data = {
        "text": random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/comments/{comment['id']}",
        headers=token,
        json=data
    )
    updated_comment = response.json()

    assert response.status_code == 200
    assert updated_comment["id"] == comment["id"]
    assert updated_comment["is_modified"] == True
    assert updated_comment["text"] == data["text"]


def test_update_not_existing_comment():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    data = {
        "text": random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/comments/{comment['id'] + 1}",
        headers=token,
        json=data
    )

    assert response.status_code == 404


def test_update_deactivated_comment():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    deactivate_comment(id=comment["id"], token=token)

    data = {
        "text": random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/comments/{comment['id']}",
        headers=token,
        json=data
    )

    assert response.status_code == 404


def test_unauthorized_update_comment():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    new_username = random_lower_string()
    new_password = random_lower_string()

    new_token = create_random_user(
        username=new_username, password=new_password
    )

    data = {
        "text": random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/comments/{comment['id']}",
        headers=new_token,
        json=data
    )

    assert response.status_code == 401


def test_delete_comment_as_superuser():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.delete(
        f"{settings.API_V1_STR}/comments/{comment['id']}",
        headers=superuser_token,
    )

    assert response.status_code == 200


def test_delete_comment_as_normal_user():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/comments/{comment['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_delete_not_existing_comment():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/comments/{comment['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_activate_comment_as_superuser():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    random_comment = create_random_comment(post_id=post["id"], token=token)

    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.put(
        f"{settings.API_V1_STR}/comments/activate/{random_comment['id']}",
        headers=superuser_token,
    )
    comment = response.json()

    assert response.status_code == 200
    assert comment["is_active"] == True


def test_activate_comment_as_normal_user():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    response = client.put(
        f"{settings.API_V1_STR}/comments/activate/{comment['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_activate_not_existing_comment():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    response = client.put(
        f"{settings.API_V1_STR}/comments/activate/{comment['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_deactivate_comment_as_superuser():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    random_comment = create_random_comment(post_id=post["id"], token=token)

    superuser_token = authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.put(
        f"{settings.API_V1_STR}/comments/deactivate/{random_comment['id']}",
        headers=superuser_token,
    )
    comment = response.json()

    assert response.status_code == 200
    assert comment["is_active"] == False


def test_deactivate_comment_as_normal_user():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    random_comment = create_random_comment(post_id=post["id"], token=token)

    response = client.put(
        f"{settings.API_V1_STR}/comments/deactivate/{random_comment['id']}",
        headers=token,
    )
    comment = response.json()

    assert response.status_code == 200
    assert comment["is_active"] == False


def test_deactivate_not_existing_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    response = client.put(
        f"{settings.API_V1_STR}/comments/deactivate/{comment['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_unauthorized_deactivate_comment():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    new_username = random_lower_string()
    new_password = random_lower_string()

    new_token = create_random_user(
        username=new_username, password=new_password
    )

    response = client.put(
        f"{settings.API_V1_STR}/comments/deactivate/{comment['id']}",
        headers=new_token,
    )

    assert response.status_code == 401


def test_deactivated_comment_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    post_comments_count = get_post(post_id=post["id"])["comments"]

    deactivate_comment(id=comment["id"], token=token)

    new_post_comments_count = get_post(post_id=post["id"])["comments"]

    assert new_post_comments_count == post_comments_count - 1


# def test_deactivated_comment_likes():
#     username = random_lower_string()
#     password = random_lower_string()

#     token = create_random_user(username=username, password=password)
#     post = create_random_post(token=token)
#     comment = create_random_comment(post_id=post["id"], token=token)

#     like_comment(comment_id=comment["id"], token=token)

#     comment_likes_count = active_likes_by_comment_id(comment_id=comment["id"])

#     deactivate_comment(id=comment["id"], token=token)

#     new_comment_likes_count = active_likes_by_comment_id(
#         comment_id=comment["id"]
#     )

#     assert new_comment_likes_count == comment_likes_count - 1


def test_get_all_active_comments_count():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    create_random_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/comments/count/",
    )
    count = response.json()

    assert response.status_code == 200
    assert count > 0


def test_get_all_active_comments_count_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    count = all_active_comments_count()
    deactivate_comment(id=comment["id"], token=token)
    new_count = all_active_comments_count()

    assert new_count == count - 1


def test_get_all_active_comments_ids():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    create_random_comment(post_id=post["id"], token=token)

    count = client.get(
        f"{settings.API_V1_STR}/comments/count/"
    ).json()

    response = client.get(
        f"{settings.API_V1_STR}/comments/ids/?limit={count + 10}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == count


def test_get_all_active_comments_ids_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    count = all_active_comments_count()
    ids = all_active_comments_ids(count=count)
    deactivate_comment(id=comment["id"], token=token)
    new_count = all_active_comments_count()
    new_ids = all_active_comments_ids(count=new_count)

    assert len(new_ids) == len(ids) - 1


def test_get_active_comments_count_by_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)
    post = create_random_post(token=token)
    create_random_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/comments/owner/count/{user['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_active_comments_count_by_owner_id_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    count = active_comments_count_by_owner_id(owner_id=user["id"])
    deactivate_comment(id=comment["id"], token=token)
    new_count = active_comments_count_by_owner_id(owner_id=user["id"])

    assert new_count == count - 1


def test_get_active_comments_count_by_not_existing_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/comments/owner/count/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_comments_ids_by_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)
    post = create_random_post(token=token)
    create_random_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/comments/owner/ids/{user['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_active_comments_ids_by_owner_id_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    ids = active_comments_ids_by_owner_id(owner_id=user["id"])
    deactivate_comment(id=comment["id"], token=token)
    new_ids = active_comments_ids_by_owner_id(owner_id=user["id"])

    assert len(new_ids) == len(ids) - 1


def test_get_active_comments_ids_by_not_existing_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/comments/owner/ids/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_comments_count_by_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    create_random_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/comments/post/count/{post['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_active_comments_count_by_post_id_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    count = active_comments_count_by_post_id(post_id=post["id"])
    deactivate_comment(id=comment["id"], token=token)
    new_count = active_comments_count_by_post_id(post_id=post["id"])

    assert new_count == count - 1


def test_get_active_comments_count_by_not_existing_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/comments/post/count/{post['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_comments_ids_by_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    create_random_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/comments/post/ids/{post['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_active_comments_ids_by_post_id_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    ids = active_comments_ids_by_post_id(post_id=post["id"])
    deactivate_comment(id=comment["id"], token=token)
    new_ids = active_comments_ids_by_post_id(post_id=post["id"])

    assert len(new_ids) == len(ids) - 1


def test_get_active_comments_ids_by_not_existing_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/comments/post/ids/{post['id'] + 1}",
    )

    assert response.status_code == 404
