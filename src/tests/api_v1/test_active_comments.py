from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import utils


def test_get_all_active_comments():
    response = client.get(
        f"{settings.API_V1_STR}/active-comments/all/",
    )

    assert response.status_code == 200


def test_get_all_active_comments_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    count = utils.get_all_active_comments_count()
    utils.deactivate_comment(comment_id=comment["id"], token=token)
    new_count = utils.get_all_active_comments_count()

    assert new_count == count - 1


def test_get_active_comment_by_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/{comment['id']}",
    )
    response_comment = response.json()

    assert response.status_code == 200
    assert response_comment == comment


def test_get_not_existing_comment_by_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/{comment['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_deactivated_comment_by_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    utils.deactivate_comment(comment_id=comment["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/{comment['id']}",
    )

    assert response.status_code == 404


def test_get_all_active_comments_count():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/count/",
    )
    count = response.json()

    assert response.status_code == 200
    assert count > 0


def test_get_all_active_comments_count_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    count = utils.get_all_active_comments_count()
    utils.deactivate_comment(comment_id=comment["id"], token=token)
    new_count = utils.get_all_active_comments_count()

    assert new_count == count - 1


def test_get_all_active_comments_ids():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)

    count = utils.get_all_active_comments_count()

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/ids/?limit={count + 10}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == count


def test_get_all_active_comments_ids_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    count = utils.get_all_active_comments_count()
    ids = utils.get_all_active_comments_ids(count=count)
    utils.deactivate_comment(comment_id=comment["id"], token=token)
    new_count = utils.get_all_active_comments_count()
    new_ids = utils.get_all_active_comments_ids(count=new_count)

    assert len(new_ids) == len(ids) - 1


def test_get_active_comments_count_by_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/owner/count/{user['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_active_comments_count_by_owner_id_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    count = utils.get_active_comments_count_by_owner_id(owner_id=user["id"])
    utils.deactivate_comment(comment_id=comment["id"], token=token)
    new_count = utils.get_active_comments_count_by_owner_id(
        owner_id=user["id"]
    )

    assert count == 1
    assert new_count == 0


def test_get_active_comments_count_by_not_existing_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/owner/count/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_comments_count_by_deactivated_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    utils.deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/owner/count/{user['id']}",
    )

    assert response.status_code == 404


def test_get_active_comments_ids_by_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/owner/ids/{user['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_active_comments_ids_by_owner_id_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    ids = utils.get_active_comments_ids_by_owner_id(owner_id=user["id"])
    utils.deactivate_comment(comment_id=comment["id"], token=token)
    new_ids = utils.get_active_comments_ids_by_owner_id(owner_id=user["id"])

    assert len(ids) == 1
    assert len(new_ids) == 0


def test_get_active_comments_ids_by_not_existing_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/owner/ids/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_comments_ids_by_deactivated_owner_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    user = utils.get_active_user(username=username)
    utils.deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/owner/ids/{user['id']}",
    )

    assert response.status_code == 404


def test_get_active_comments_count_by_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/post/count/{post['id']}",
    )
    count = response.json()

    assert response.status_code == 200
    assert count == 1


def test_get_active_comments_count_by_post_id_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    count = utils.get_active_comments_count_by_post_id(post_id=post["id"])
    utils.deactivate_comment(comment_id=comment["id"], token=token)
    new_count = utils.get_active_comments_count_by_post_id(post_id=post["id"])

    assert count == 1
    assert new_count == 0


def test_get_active_comments_count_by_not_existing_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/post/count/{post['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_comments_count_by_deactivated_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.deactivate_post(post_id=post['id'], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/post/count/{post['id']}",
    )

    assert response.status_code == 404


def test_get_active_comments_ids_by_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.create_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/post/ids/{post['id']}",
    )
    ids = response.json()

    assert response.status_code == 200
    assert len(ids) == 1


def test_get_active_comments_ids_by_post_id_is_all_active():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    comment = utils.create_comment(post_id=post["id"], token=token)

    ids = utils.get_active_comments_ids_by_post_id(post_id=post["id"])
    utils.deactivate_comment(comment_id=comment["id"], token=token)
    new_ids = utils.get_active_comments_ids_by_post_id(post_id=post["id"])

    assert len(ids) == 1
    assert len(new_ids) == 0


def test_get_active_comments_ids_by_not_existing_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/post/ids/{post['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_comments_ids_by_deactivated_post_id():
    username = utils.random_lower_string()
    password = utils.random_lower_string()

    token = utils.create_user(username=username, password=password)
    post = utils.create_post(token=token)
    utils.deactivate_post(post_id=post['id'], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/post/ids/{post['id']}",
    )

    assert response.status_code == 404
