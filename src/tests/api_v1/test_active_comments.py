from src.core.config import settings
from src.tests.conftest import client
from src.tests.utils import (create_random_comment, create_random_post,
                             create_random_user, deactivate_comment,
                             deactivate_post, deactivate_user,
                             get_active_comments_count_by_owner_id,
                             get_active_comments_count_by_post_id,
                             get_active_comments_ids_by_owner_id,
                             get_active_comments_ids_by_post_id,
                             get_active_user, get_all_active_comments_count,
                             get_all_active_comments_ids, random_lower_string)


def test_get_all_active_comments():
    response = client.get(
        f"{settings.API_V1_STR}/active-comments/all/",
    )

    assert response.status_code == 200


def test_get_all_active_comments_is_all_active():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    count = get_all_active_comments_count()
    deactivate_comment(id=comment["id"], token=token)
    new_count = get_all_active_comments_count()

    assert new_count == count - 1


def test_get_active_comment_by_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/{comment['id']}",
    )
    response_comment = response.json()

    assert response.status_code == 200
    assert response_comment == comment


def test_get_not_existing_comment_by_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    comment = create_random_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/{comment['id'] + 1}",
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
        f"{settings.API_V1_STR}/active-comments/{comment['id']}",
    )

    assert response.status_code == 404


def test_get_get_all_active_comments_count():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    create_random_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/count/",
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

    count = get_all_active_comments_count()
    deactivate_comment(id=comment["id"], token=token)
    new_count = get_all_active_comments_count()

    assert new_count == count - 1


def test_get_all_active_comments_ids():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    create_random_comment(post_id=post["id"], token=token)

    count = get_all_active_comments_count()

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/ids/?limit={count + 10}",
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

    count = get_all_active_comments_count()
    ids = get_all_active_comments_ids(count=count)
    deactivate_comment(id=comment["id"], token=token)
    new_count = get_all_active_comments_count()
    new_ids = get_all_active_comments_ids(count=new_count)

    assert len(new_ids) == len(ids) - 1


def test_get_active_comments_count_by_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)
    post = create_random_post(token=token)
    create_random_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/owner/count/{user['id']}",
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

    count = get_active_comments_count_by_owner_id(owner_id=user["id"])
    deactivate_comment(id=comment["id"], token=token)
    new_count = get_active_comments_count_by_owner_id(owner_id=user["id"])

    assert new_count == count - 1


def test_get_active_comments_count_by_not_existing_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/owner/count/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_comments_count_by_deactivated_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)
    deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/owner/count/{user['id']}",
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
        f"{settings.API_V1_STR}/active-comments/owner/ids/{user['id']}",
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

    ids = get_active_comments_ids_by_owner_id(owner_id=user["id"])
    deactivate_comment(id=comment["id"], token=token)
    new_ids = get_active_comments_ids_by_owner_id(owner_id=user["id"])

    assert len(new_ids) == len(ids) - 1


def test_get_active_comments_ids_by_not_existing_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user(username=username, password=password)
    user = get_active_user(username=username)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/owner/ids/{user['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_comments_ids_by_deactivated_owner_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    user = get_active_user(username=username)
    deactivate_user(username=username, token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/owner/ids/{user['id']}",
    )

    assert response.status_code == 404


def test_get_active_comments_count_by_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    create_random_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/post/count/{post['id']}",
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

    count = get_active_comments_count_by_post_id(post_id=post["id"])
    deactivate_comment(id=comment["id"], token=token)
    new_count = get_active_comments_count_by_post_id(post_id=post["id"])

    assert new_count == count - 1


def test_get_active_comments_count_by_not_existing_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/post/count/{post['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_comments_count_by_deactivated_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    deactivate_post(id=post['id'], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/post/count/{post['id']}",
    )

    assert response.status_code == 404


def test_get_active_comments_ids_by_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    create_random_comment(post_id=post["id"], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/post/ids/{post['id']}",
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

    ids = get_active_comments_ids_by_post_id(post_id=post["id"])
    deactivate_comment(id=comment["id"], token=token)
    new_ids = get_active_comments_ids_by_post_id(post_id=post["id"])

    assert len(new_ids) == len(ids) - 1


def test_get_active_comments_ids_by_not_existing_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/post/ids/{post['id'] + 1}",
    )

    assert response.status_code == 404


def test_get_active_comments_ids_by_deactivated_post_id():
    username = random_lower_string()
    password = random_lower_string()

    token = create_random_user(username=username, password=password)
    post = create_random_post(token=token)
    deactivate_post(id=post['id'], token=token)

    response = client.get(
        f"{settings.API_V1_STR}/active-comments/post/ids/{post['id']}",
    )

    assert response.status_code == 404
