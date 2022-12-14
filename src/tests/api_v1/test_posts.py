from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import utils


def test_create_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    data = {
        "text": utils.random_lower_string()
    }

    response = client.post(
        f"{settings.API_V1_STR}/posts/",
        headers=token,
        json=data
    )
    post = response.json()

    assert response.status_code == 200
    assert post["text"] == data["text"]
    assert post["owner_id"] == user["id"]


def test_user_posts_count_after_post_created():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    utils.create_post(token=token)
    user = utils.get_active_user(username=username)

    assert user["posts"] == 1


def test_update_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    data = {
        "text": utils.random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/posts/{post['id']}",
        headers=token,
        json=data
    )
    updated_post = response.json()

    assert response.status_code == 200
    assert updated_post["id"] == post["id"]
    assert updated_post["is_modified"] == True
    assert updated_post["text"] == data["text"]


def test_update_not_existing_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    data = {
        "text": utils.random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/posts/{post['id'] + 1}",
        headers=token,
        json=data
    )

    assert response.status_code == 404


def test_update_deactivated_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    utils.deactivate_post(post_id=post["id"], token=token)

    data = {
        "text": utils.random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/posts/{post['id']}",
        headers=token,
        json=data
    )

    assert response.status_code == 404


def test_unauthorized_update_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    new_username = utils.random_lower_string()
    new_password = utils.random_lower_string()

    new_token = utils.create_user(
        username=new_username, password=new_password
    )

    data = {
        "text": utils.random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/posts/{post['id']}",
        headers=new_token,
        json=data
    )

    assert response.status_code == 401


def test_delete_post_as_superuser():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.delete(
        f"{settings.API_V1_STR}/posts/{post['id']}",
        headers=superuser_token,
    )

    assert response.status_code == 200


def test_delete_post_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/posts/{post['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_delete_not_existing_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/posts/{post['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_delete_deactivated_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    utils.deactivate_post(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.delete(
        f"{settings.API_V1_STR}/posts/{post['id']}",
        headers=superuser_token,
    )

    assert response.status_code == 200


def test_user_posts_count_after_post_deleted():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.delete_post(post_id=post["id"])
    user = utils.get_active_user(username=username)

    assert user["posts"] == 0


def test_activate_post_as_superuser():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.deactivate_post(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.put(
        f"{settings.API_V1_STR}/posts/activate/{post['id']}",
        headers=superuser_token,
    )
    response_post = response.json()

    assert response.status_code == 200
    assert response_post["is_active"] == True


def test_activate_post_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    response = client.put(
        f"{settings.API_V1_STR}/posts/activate/{post['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_activate_not_existing_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    response = client.put(
        f"{settings.API_V1_STR}/posts/activate/{post['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_post_likes_count_after_post_activated():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.like_post(post_id=post["id"], token=token)

    utils.deactivate_post(post_id=post["id"], token=token)
    utils.activate_post(post_id=post["id"])

    activated_post = utils.get_active_post(post_id=post["id"])

    assert activated_post["likes"] == 1


def test_post_comments_count_after_post_activated():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)

    utils.deactivate_post(post_id=post["id"], token=token)
    utils.activate_post(post_id=post["id"])

    activated_post = utils.get_active_post(post_id=post["id"])

    assert activated_post["comments"] == 1


def test_user_posts_count_after_post_activated():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    utils.deactivate_post(post_id=post["id"], token=token)
    utils.activate_post(post_id=post["id"])

    user = utils.get_active_user(username=username)

    assert user["posts"] == 1


def test_deactivate_post_as_superuser():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    random_post = utils.create_post(token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.put(
        f"{settings.API_V1_STR}/posts/deactivate/{random_post['id']}",
        headers=superuser_token,
    )
    post = response.json()

    assert response.status_code == 200
    assert post["is_active"] == False


def test_deactivate_post_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    random_post = utils.create_post(token=token)

    response = client.put(
        f"{settings.API_V1_STR}/posts/deactivate/{random_post['id']}",
        headers=token,
    )
    post = response.json()

    assert response.status_code == 200
    assert post["is_active"] == False


def test_deactivate_not_existing_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    response = client.put(
        f"{settings.API_V1_STR}/posts/deactivate/{post['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_user_posts_count_after_deactivated_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.deactivate_post(post_id=post["id"], token=token)
    user = utils.get_active_user(username=username)

    assert user["posts"] == 0


def test_unauthorized_deactivate_post():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    new_username = utils.random_lower_string()
    new_password = utils.random_lower_string()

    new_token = utils.create_user(
        username=new_username, password=new_password
    )

    response = client.put(
        f"{settings.API_V1_STR}/posts/deactivate/{post['id']}",
        headers=new_token
    )

    assert response.status_code == 401


def test_get_all_posts_as_super_user():
    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/posts/all/",
        headers=superuser_token,
    )

    assert response.status_code == 200


def test_get_all_posts_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/posts/all/",
        headers=token,
    )

    assert response.status_code == 401


def test_get_all_posts_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    all_posts_count = utils.get_all_posts_count()
    utils.deactivate_post(post_id=post["id"], token=token)
    new_all_posts_count = utils.get_all_posts_count()

    assert new_all_posts_count == all_posts_count


def test_get_post_by_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/posts/{post['id']}",
        headers=superuser_token,
    )
    response_post = response.json()

    assert response.status_code == 200
    assert response_post == post


def test_get_post_by_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/posts/{post['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_not_existing_post_by_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/posts/{post['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_deleted_post_by_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    utils.delete_post(post_id=post["id"])

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/posts/{post['id']}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_deactivated_post_by_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    utils.deactivate_post(post_id=post["id"], token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/posts/{post['id']}",
        headers=superuser_token,
    )
    response_post = response.json()

    assert response.status_code == 200
    assert response_post["id"] == post["id"]
    assert response_post["is_active"] == False


def test_get_all_posts_count_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    utils.create_post(token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/posts/count/",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count > 0


def test_get_all_posts_count_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    utils.create_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/posts/count/",
        headers=token,
    )

    assert response.status_code == 401


def test_get_all_posts_count_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    all_posts_count = utils.get_all_posts_count()
    utils.deactivate_post(post_id=post["id"], token=token)
    new_all_posts_count = utils.get_all_posts_count()

    assert new_all_posts_count == all_posts_count


def test_get_all_posts_ids_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    utils.create_post(token=token)

    count = utils.get_all_posts_count()

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/posts/ids/?limit={count + 10}",
        headers=superuser_token,
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == count


def test_get_all_posts_ids_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    utils.create_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/posts/ids/",
        headers=token,
    )

    assert response.status_code == 401


def test_get_all_posts_ids_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    count = utils.get_all_posts_count()
    ids = utils.get_all_posts_ids(count=count)
    utils.deactivate_post(post_id=post["id"], token=token)
    new_count = utils.get_all_posts_count()
    new_ids = utils.get_all_posts_ids(count=new_count)

    assert new_ids == ids


def test_get_posts_count_by_owner_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    utils.create_post(token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/count/{user['id']}",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_posts_count_by_owner_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/count/{user['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_posts_count_by_owner_id_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    post = utils.create_post(token=token)

    count = utils.get_posts_count_by_owner_id(owner_id=user["id"])
    utils.deactivate_post(post_id=post["id"], token=token)
    new_count = utils.get_posts_count_by_owner_id(owner_id=user["id"])

    assert count == 1
    assert new_count == 1


def test_get_posts_count_by_not_existing_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/count/{user['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_posts_count_by_deactivated_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    utils.create_post(token=token)
    utils.deactivate_user(username=username, token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/count/{user['id']}",
        headers=superuser_token,
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_posts_ids_by_owner_id_as_super_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    utils.create_post(token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/ids/{user['id']}",
        headers=superuser_token,
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_posts_ids_by_owner_id_as_normal_user():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/ids/{user['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_get_posts_ids_by_owner_id_is_all():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    post = utils.create_post(token=token)

    ids = utils.get_posts_ids_by_owner_id(owner_id=user["id"])
    utils.deactivate_post(post_id=post["id"], token=token)
    new_ids = utils.get_posts_ids_by_owner_id(owner_id=user["id"])

    assert len(ids) == 1
    assert len(new_ids) == 1


def test_get_posts_ids_by_not_existing_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/ids/{user['id'] + 1}",
        headers=superuser_token,
    )

    assert response.status_code == 404


def test_get_posts_ids_by_deactivated_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    utils.create_post(token=token)

    ids = utils.get_posts_ids_by_owner_id(owner_id=user["id"])
    utils.deactivate_user(username=username, token=token)

    superuser_token = utils.authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/ids/{user['id']}",
        headers=superuser_token,
    )
    response_ids = response.json()

    assert response.status_code == 200
    assert response_ids == ids
