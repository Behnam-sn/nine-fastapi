from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import (create_random_post, create_random_user,
                             get_random_user, random_lower_string,
                             user_authentication_headers)


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


def test_get_all_posts():
    response = client.get(
        f"{settings.API_V1_STR}/posts/all/",
    )

    assert response.status_code == 200


def test_get_post_by_id():
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


def test_delete_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    random_post = create_random_post(token=token)

    response = client.delete(
        f"{settings.API_V1_STR}/posts/{random_post['id']}",
        headers=token,
    )

    assert response.status_code == 400


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


def test_activate_post():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    random_post = create_random_post(token=token)

    response = client.put(
        f"{settings.API_V1_STR}/posts/activate/{random_post['id']}",
        headers=token,
    )

    assert response.status_code == 400


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


def test_deactivate_post():
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


def test_get_all_posts_count():
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


def test_get_all_posts_ids():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    create_random_post(token=token)

    count = client.get(
        f"{settings.API_V1_STR}/posts/count/"
    ).json()

    response = client.get(
        f"{settings.API_V1_STR}/posts/ids/",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == count


def test_get_posts_count_by_owner_id():
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


def test_get_posts_count_by_not_existing_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    user = get_random_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/count/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_posts_ids_by_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_random_user(username=username)
    create_random_post(token=token)

    count = client.get(
        f"{settings.API_V1_STR}/posts/owner/count/{user['id']}"
    ).json()

    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/ids/{user['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == count


def test_get_posts_ids_by_not_existing_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    user = get_random_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/posts/owner/ids/{user['id'] + 1}",
    )

    assert response.status_code == 404
