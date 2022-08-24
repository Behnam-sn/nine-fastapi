from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import (active_posts_count_by_owner_id,
                             active_posts_ids_by_owner_id,
                             all_active_posts_count, all_active_posts_ids,
                             create_random_post, create_random_user,
                             deactive_post, get_random_user,
                             random_lower_string, user_authentication_headers)


def test_create_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_random_user(username=username)

    data = {
        "text": random_lower_string()
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


def test_get_all_active_posts():
    response = client.get(
        f"{settings.API_V1_STR}/posts/all/",
    )

    assert response.status_code == 200


def test_get_active_post_by_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    random_post = create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/posts/{random_post['id']}",
    )
    post = response.json()

    assert response.status_code == 200
    assert random_post == post


def test_get_not_existing_post_by_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/posts/{post['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_deactivated_post_by_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    deactive_post(id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/posts/{post['id']}",
    )

    assert response.status_code == 403


def test_update_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    random_post = create_random_post(token=token)

    data = {
        "text": random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/posts/{random_post['id']}",
        headers=token,
        json=data
    )
    post = response.json()

    assert response.status_code == 200
    assert post["id"] == random_post["id"]
    assert post["is_modified"] == True
    assert post["text"] == data["text"]


def test_update_not_existing_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    data = {
        "text": random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/posts/{post['id'] + 1}",
        headers=token,
        json=data
    )

    assert response.status_code == 404


def test_update_deactivated_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    deactive_post(id=post["id"], token=token)

    data = {
        "text": random_lower_string()
    }

    response = client.get(
        f"{settings.API_V1_STR}/posts/{post['id']}",
        headers=token,
        json=data
    )

    assert response.status_code == 403


def test_unauthorized_update_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    new_username = random_lower_string()
    new_password = random_lower_string()

    new_token = create_random_user(
        username=new_username, password=new_password
    )

    data = {
        "text": random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/posts/{post['id']}",
        headers=new_token,
        json=data
    )

    assert response.status_code == 401


def test_delete_post_as_superuser():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    random_post = create_random_post(token=token)

    superuser_token = user_authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.delete(
        f"{settings.API_V1_STR}/posts/{random_post['id']}",
        headers=superuser_token,
    )

    assert response.status_code == 200


def test_delete_post_as_normal_user():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    random_post = create_random_post(token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/posts/{random_post['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_delete_not_existing_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    random_post = create_random_post(token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/posts/{random_post['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_activate_post_as_superuser():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    random_post = create_random_post(token=token)

    superuser_token = user_authentication_headers(
        username=settings.SUPERUSER_USERNAME,
        password=settings.SUPERUSER_PASSWORD
    )

    response = client.put(
        f"{settings.API_V1_STR}/posts/activate/{random_post['id']}",
        headers=superuser_token,
    )
    post = response.json()

    assert response.status_code == 200
    assert post["is_active"] == True


def test_activate_post_as_normal_user():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    random_post = create_random_post(token=token)

    response = client.put(
        f"{settings.API_V1_STR}/posts/activate/{random_post['id']}",
        headers=token,
    )

    assert response.status_code == 401


def test_activate_not_existing_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    random_post = create_random_post(token=token)

    response = client.put(
        f"{settings.API_V1_STR}/posts/activate/{random_post['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_deactivate_post_as_superuser():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    random_post = create_random_post(token=token)

    superuser_token = user_authentication_headers(
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
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    random_post = create_random_post(token=token)

    response = client.put(
        f"{settings.API_V1_STR}/posts/deactivate/{random_post['id']}",
        headers=token,
    )
    post = response.json()

    assert response.status_code == 200
    assert post["is_active"] == False


def test_deactivate_not_existing_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    random_post = create_random_post(token=token)

    response = client.put(
        f"{settings.API_V1_STR}/posts/deactivate/{random_post['id'] + 1}",
        headers=token,
    )

    assert response.status_code == 404


def test_unauthorized_deactivate_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    new_username = random_lower_string()
    new_password = random_lower_string()

    new_token = create_random_user(
        username=new_username, password=new_password
    )

    response = client.put(
        f"{settings.API_V1_STR}/posts/deactivate/{post['id']}",
        headers=new_token
    )

    assert response.status_code == 401


def test_get_all_active_posts_count():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/posts/count/",
    )
    count = response.json()

    assert response.status_code == 200
    assert count > 0


def test_get_all_active_posts_count_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    count = all_active_posts_count()

    deactive_post(id=post["id"], token=token)

    new_count = all_active_posts_count()

    assert new_count == count - 1


def test_get_all_active_posts_ids():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    create_random_post(token=token)

    count = client.get(
        f"{settings.API_V1_STR}/posts/count/"
    ).json()

    response = client.get(
        f"{settings.API_V1_STR}/posts/ids/?limit={count + 10}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == count


def test_get_all_active_posts_ids_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    count = all_active_posts_count()
    ids = all_active_posts_ids(count=count)

    deactive_post(id=post["id"], token=token)

    new_count = all_active_posts_count()
    new_ids = all_active_posts_ids(count=new_count)

    assert len(new_ids) == len(ids) - 1


def test_get_active_posts_count_by_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_random_user(username=username)
    create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/count/{user['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_active_posts_count_by_owner_id_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_random_user(username=username)
    post = create_random_post(token=token)

    deactive_post(id=post["id"], token=token)
    count = active_posts_count_by_owner_id(owner_id=user["id"])

    assert count == 0


def test_get_active_posts_count_by_not_existing_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    user = get_random_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/count/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_posts_ids_by_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_random_user(username=username)
    create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/ids/{user['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_active_posts_ids_by_owner_id_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_random_user(username=username)
    post = create_random_post(token=token)

    deactive_post(id=post["id"], token=token)
    ids = active_posts_ids_by_owner_id(owner_id=user["id"])

    assert len(ids) == 0


def test_get_active_posts_ids_by_not_existing_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    user = get_random_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/ids/{user['id'] + 1}",
    )

    assert response.status_code == 404
