from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import utils


def test_create_comment():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_post(token=token)

    data = {
        "text": utils.random_lower_string(),
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


def test_post_comments_count_after_created_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)
    updated_post = utils.get_active_post(post_id=post["id"])

    assert updated_post["comments"] == 1


def test_comment_on_not_existing_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    data = {
        "text": utils.random_lower_string(),
        "post_id": post["id"] + 1
    }

    response = client.post(
        f"{settings.API_V1_STR}/comments/",
        headers=token,
        json=data
    )

    assert response.status_code == 404


def test_comment_on_deactivated_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.deactivate_post(post_id=post["id"], token=token)

    data = {
        "text": utils.random_lower_string(),
        "post_id": post["id"]
    }

    response = client.post(
        f"{settings.API_V1_STR}/comments/",
        headers=token,
        json=data
    )

    assert response.status_code == 404


def test_update_comment():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    data = {
        "text": utils.random_lower_string()
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
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    data = {
        "text": utils.random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/comments/{comment['id'] + 1}",
        headers=token,
        json=data
    )

    assert response.status_code == 404


def test_update_deactivated_comment():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.deactivate_comment(comment_id=comment["id"], token=token)

    data = {
        "text": utils.random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/comments/{comment['id']}",
        headers=token,
        json=data
    )

    assert response.status_code == 404


def test_unauthorized_update_comment():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    new_username = utils.random_lower_string()
    new_password = utils.random_lower_string()

    new_token = utils.create_user(
        username=new_username, password=new_password
    )

    data = {
        "text": utils.random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/comments/{comment['id']}",
        headers=new_token,
        json=data
    )

    assert response.status_code == 401


def test_delete_comment_as_superuser():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.delete(
        f"{settings.API_V1_STR}/comments/{comment['id']}",
        headers=superuser_token,
    )

    assert response.status_code == 200


def test_delete_comment_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/comments/{comment['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_delete_not_existing_comment():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/comments/{comment['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_delete_deactivated_comment():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.deactivate_comment(comment_id=comment["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.delete(
        f"{settings.API_V1_STR}/comments/{comment['id']}",
        headers=superuser_token,
    )

    assert response.status_code == 200


def test_post_comments_count_after_comment_deleted():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)
    utils.delete_comment(comment_id=comment["id"])
    updated_post = utils.get_active_post(post_id=post["id"])

    assert updated_post["comments"] == 0


def test_activate_comment_as_superuser():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    random_comment = utils.create_comment(
        post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
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
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    response = client.put(
        f"{settings.API_V1_STR}/comments/activate/{comment['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_activate_not_existing_comment():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    response = client.put(
        f"{settings.API_V1_STR}/comments/activate/{comment['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_comment_likes_count_after_comment_activated():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)
    utils.like_comment(comment_id=comment["id"], token=token)

    utils.deactivate_comment(comment_id=comment["id"], token=token)
    utils.activate_comment(comment_id=comment["id"])

    activated_comment = utils.get_active_comment(comment_id=comment["id"])

    assert activated_comment["likes"] == 1


def test_post_comments_count_after_comment_activated():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.deactivate_comment(comment_id=comment["id"], token=token)
    utils.activate_comment(comment_id=comment["id"])

    updated_post = utils.get_active_post(post_id=post["id"])

    assert updated_post["comments"] == 1


def test_deactivate_comment_as_superuser():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    random_comment = utils.create_comment(
        post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
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
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    random_comment = utils.create_comment(
        post_id=post["id"], token=token)

    response = client.put(
        f"{settings.API_V1_STR}/comments/deactivate/{random_comment['id']}",
        headers=token,
    )
    comment = response.json()

    assert response.status_code == 200
    assert comment["is_active"] == False


def test_deactivate_not_existing_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    response = client.put(
        f"{settings.API_V1_STR}/comments/deactivate/{comment['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_unauthorized_deactivate_comment():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    new_username = utils.random_lower_string()
    new_password = utils.random_lower_string()

    new_token = utils.create_user(
        username=new_username, password=new_password
    )

    response = client.put(
        f"{settings.API_V1_STR}/comments/deactivate/{comment['id']}",
        headers=new_token,
    )

    assert response.status_code == 401


def test_post_comments_count_after_comment_deactivated():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.deactivate_comment(comment_id=comment["id"], token=token)

    updated_post = utils.get_active_post(post_id=post["id"])

    assert updated_post["comments"] == 0


def test_get_all_comments_as_super_user():
    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/all/",
        headers=superuser_token,
    )

    assert response.status_code == 200


def test_get_all_comments_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/comments/all/",
        headers=token,
    )

    assert response.status_code == 401


def test_get_all_comments_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    count = utils.get_all_comments_count()
    utils.deactivate_comment(comment_id=comment["id"], token=token)
    new_count = utils.get_all_comments_count()

    assert new_count == count


def test_get_comment_by_id_as_super_user():
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
        f"{settings.API_V1_STR}/comments/{comment['id']}",
        headers=superuser_token,
    )
    response_comment = response.json()

    assert response.status_code == 200
    assert response_comment == comment


def test_get_comment_by_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/comments/{comment['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_not_existing_comment_by_id():
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
        f"{settings.API_V1_STR}/comments/{comment['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


# def test_get_deleted_comment_by_id():
#     pass


def test_get_deactivated_comment_by_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.deactivate_comment(comment_id=comment["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/{comment['id']}",
        headers=superuser_token,
    )
    response_comment = response.json()

    assert response.status_code == 200
    assert response_comment["id"] == comment["id"]
    assert response_comment["is_active"] == False


def test_get_all_comments_count_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/count/",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count > 0


def test_get_all_comments_count_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/comments/count/",
        headers=token,
    )

    assert response.status_code == 401


def test_get_all_comments_count_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    count = utils.get_all_comments_count()
    utils.deactivate_comment(comment_id=comment["id"], token=token)
    new_count = utils.get_all_comments_count()

    assert new_count == count


def test_get_all_comments_ids_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)

    count = utils.get_all_comments_count()

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/ids/?limit={count + 10}",
        headers=superuser_token,
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == count


def test_get_all_comments_ids_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/comments/ids/",
        headers=token,
    )

    assert response.status_code == 401


def test_get_all_comments_ids_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    count = utils.get_all_comments_count()
    ids = utils.get_all_comments_ids(count=count)
    utils.deactivate_comment(comment_id=comment["id"], token=token)
    new_count = utils.get_all_comments_count()
    new_ids = utils.get_all_comments_ids(count=new_count)

    assert new_ids == ids


def test_get_comments_count_by_owner_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_user(username=username)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/owner/count/{user['id']}",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_comments_count_by_owner_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/comments/owner/count/{user['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_comments_count_by_owner_id_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_user(username=username)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    count = utils.get_comments_count_by_owner_id(owner_id=user["id"])
    utils.deactivate_comment(comment_id=comment["id"], token=token)
    new_count = utils.get_comments_count_by_owner_id(owner_id=user["id"])

    assert new_count == count


def test_get_comments_count_by_not_existing_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)
    user = utils.get_user(username=username)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/owner/count/{user['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_comment_count_by_deactivated_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_user(username=username)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)
    utils.deactivate_user(username=username, token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/owner/count/{user['id']}",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_comments_ids_by_owner_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_user(username=username)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/owner/ids/{user['id']}",
        headers=superuser_token,
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_comments_ids_by_owner_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/comments/owner/ids/{user['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_comments_ids_by_owner_id_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_user(username=username)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    ids = utils.get_comments_ids_by_owner_id(owner_id=user["id"])
    utils.deactivate_comment(comment_id=comment["id"], token=token)
    new_ids = utils.get_comments_ids_by_owner_id(owner_id=user["id"])

    assert new_ids == ids


def test_get_comments_ids_by_not_existing_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)
    user = utils.get_user(username=username)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/owner/ids/{user['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_comments_ids_by_deactivated_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_user(username=username)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)

    ids = utils.get_comments_ids_by_owner_id(owner_id=user["id"])
    utils.deactivate_user(username=username, token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/owner/ids/{user['id']}",
        headers=superuser_token,
    )
    response_ids = response.json()

    assert response.status_code == 200
    assert response_ids == ids


def test_get_comments_count_by_post_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/post/count/{post['id']}",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_comments_count_by_post_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/comments/post/count/{post['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_comments_count_by_post_id_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    count = utils.get_comments_count_by_post_id(post_id=post["id"])
    utils.deactivate_comment(comment_id=comment["id"], token=token)
    new_count = utils.get_comments_count_by_post_id(post_id=post["id"])

    assert new_count == count


def test_get_comments_count_by_not_existing_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/post/count/{post['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_comments_count_by_deactivated_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)
    utils.deactivate_post(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/post/count/{post['id']}",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_comments_ids_by_post_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/post/ids/{post['id']}",
        headers=superuser_token,
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_comments_ids_by_post_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/comments/post/ids/{post['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_comments_ids_by_post_id_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    ids = utils.get_comments_ids_by_post_id(post_id=post["id"])
    utils.deactivate_comment(comment_id=comment["id"], token=token)
    new_ids = utils.get_comments_ids_by_post_id(post_id=post["id"])

    assert new_ids == ids


def test_get_comments_ids_by_not_existing_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/post/ids/{post['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_comments_ids_by_deactivated_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)

    ids = utils.get_comments_ids_by_post_id(post_id=post["id"])
    utils.deactivate_post(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/comments/post/ids/{post['id']}",
        headers=superuser_token,
    )
    response_ids = response.json()

    assert response.status_code == 200
    assert response_ids == ids
