from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import (create_random_post, create_random_user,
                             deactivate_post, deactivate_user,
                             get_active_posts_count_by_owner_id,
                             get_active_posts_ids_by_owner_id, get_active_user,
                             get_all_active_posts_count,
                             get_all_active_posts_ids, random_lower_string)


def test_get_all_active_posts():
    response = client.get(
        f"{settings.API_V1_STR}/active-posts/all/",
    )

    assert response.status_code == 200


def test_get_all_active_posts_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    all_active_posts_count = get_all_active_posts_count()
    deactivate_post(id=post["id"], token=token)
    new_all_active_posts_count = get_all_active_posts_count()

    assert new_all_active_posts_count == all_active_posts_count - 1


def test_get_active_post_by_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    random_post = create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/{random_post['id']}",
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
        f"{settings.API_V1_STR}/active-posts/{post['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_deactivated_post_by_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    deactivate_post(id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/{post['id']}",
    )

    assert response.status_code == 404


def test_get_all_active_posts_count():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/count/",
    )
    count = response.json()

    assert response.status_code == 200
    assert count > 0


def test_get_all_active_posts_count_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    count = get_all_active_posts_count()
    deactivate_post(id=post["id"], token=token)
    new_count = get_all_active_posts_count()

    assert new_count == count - 1


def test_get_all_active_posts_ids():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    create_random_post(token=token)

    count = get_all_active_posts_count()

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/ids/?limit={count + 10}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == count


def test_get_all_active_posts_ids_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    count = get_all_active_posts_count()
    ids = get_all_active_posts_ids(count=count)
    deactivate_post(id=post["id"], token=token)
    new_count = get_all_active_posts_count()
    new_ids = get_all_active_posts_ids(count=new_count)

    assert len(new_ids) == len(ids) - 1


def test_get_active_posts_count_by_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)
    create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/owner/count/{user['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_active_posts_count_by_owner_id_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)
    post = create_random_post(token=token)

    count = get_active_posts_count_by_owner_id(owner_id=user["id"])
    deactivate_post(id=post["id"], token=token)
    new_count = get_active_posts_count_by_owner_id(owner_id=user["id"])

    assert new_count == count - 1


def test_get_active_posts_count_by_not_existing_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/owner/count/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_posts_count_by_deactivated_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)
    deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/owner/count/{user['id']}",
    )

    assert response.status_code == 404


def test_get_active_posts_ids_by_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)
    create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/owner/ids/{user['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_active_posts_ids_by_owner_id_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)
    post = create_random_post(token=token)

    ids = get_active_posts_ids_by_owner_id(owner_id=user["id"])
    deactivate_post(id=post["id"], token=token)
    new_ids = get_active_posts_ids_by_owner_id(owner_id=user["id"])

    assert len(new_ids) == len(ids) - 1


def test_get_active_posts_ids_by_not_existing_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/owner/ids/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_posts_ids_by_deactivated_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)
    deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/owner/ids/{user['id']}",
    )

    assert response.status_code == 404
