from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import utils


def test_get_all_active_posts():
    response = client.get(
        f"{settings.API_V1_STR}/active-posts/all/",
    )

    assert response.status_code == 200


def test_get_all_active_posts_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_random_user(username=username, password=password)
    post = utils.create_random_post(token=token)

    all_active_posts_count = utils.get_all_active_posts_count()
    utils.deactivate_post(post_id=post["id"], token=token)
    new_all_active_posts_count = utils.get_all_active_posts_count()

    assert new_all_active_posts_count == all_active_posts_count - 1


def test_get_active_post_by_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_random_user(username=username, password=password)
    random_post = utils.create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/{random_post['id']}",
    )
    post = response.json()

    assert response.status_code == 200
    assert random_post == post


def test_get_not_existing_post_by_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_random_user(username=username, password=password)
    post = utils.create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/{post['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_deactivated_post_by_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_random_user(username=username, password=password)
    post = utils.create_random_post(token=token)

    utils.deactivate_post(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/{post['id']}",
    )

    assert response.status_code == 404


def test_get_all_active_posts_count():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_random_user(username=username, password=password)
    utils.create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/count/",
    )
    count = response.json()

    assert response.status_code == 200
    assert count > 0


def test_get_all_active_posts_count_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_random_user(username=username, password=password)
    post = utils.create_random_post(token=token)

    count = utils.get_all_active_posts_count()
    utils.deactivate_post(post_id=post["id"], token=token)
    new_count = utils.get_all_active_posts_count()

    assert new_count == count - 1


def test_get_all_active_posts_ids():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_random_user(username=username, password=password)
    utils.create_random_post(token=token)

    count = utils.get_all_active_posts_count()

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/ids/?limit={count + 10}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == count


def test_get_all_active_posts_ids_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_random_user(username=username, password=password)
    post = utils.create_random_post(token=token)

    count = utils.get_all_active_posts_count()
    ids = utils.get_all_active_posts_ids(count=count)
    utils.deactivate_post(post_id=post["id"], token=token)
    new_count = utils.get_all_active_posts_count()
    new_ids = utils.get_all_active_posts_ids(count=new_count)

    assert len(new_ids) == len(ids) - 1


def test_get_active_posts_count_by_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_random_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    utils.create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/owner/count/{user['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_active_posts_count_by_owner_id_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_random_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_random_post(token=token)

    count = utils.get_active_posts_count_by_owner_id(owner_id=user["id"])
    utils.deactivate_post(post_id=post["id"], token=token)
    new_count = utils.get_active_posts_count_by_owner_id(owner_id=user["id"])

    assert new_count == count - 1


def test_get_active_posts_count_by_not_existing_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_random_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/owner/count/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_posts_count_by_deactivated_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_random_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    utils.deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/owner/count/{user['id']}",
    )

    assert response.status_code == 404


def test_get_active_posts_ids_by_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_random_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    utils.create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/owner/ids/{user['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_active_posts_ids_by_owner_id_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_random_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_random_post(token=token)

    ids = utils.get_active_posts_ids_by_owner_id(owner_id=user["id"])
    utils.deactivate_post(post_id=post["id"], token=token)
    new_ids = utils.get_active_posts_ids_by_owner_id(owner_id=user["id"])

    assert len(new_ids) == len(ids) - 1


def test_get_active_posts_ids_by_not_existing_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_random_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/owner/ids/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_posts_ids_by_deactivated_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_random_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    utils.deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-posts/owner/ids/{user['id']}",
    )

    assert response.status_code == 404
