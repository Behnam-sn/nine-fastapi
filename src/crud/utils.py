from sqlalchemy.orm import Session
from src import models


def delete_likes_by_post_id(db: Session, post_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.post_id == post_id)
        .delete()
    )


def delete_likes_by_comment_id(db: Session, comment_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.comment_id == comment_id)
        .delete()
    )


# def delete_likes_by_owner_id():
#     pass


# def delete_posts_by_owner_id():
#     pass


def activate_posts_by_owner_id(db: Session, owner_id: int):
    (
        db.query(models.Post)
        .filter(models.Post.owner_id == owner_id)
        .update({models.Post.is_owner_active: True})
    )

    posts = (
        db.query(models.Post)
        .filter(models.Post.owner_id == owner_id)
        .all()
    )

    for post in posts:
        post_dict = post.__dict__

        activate_like_post_owner_by_post_id(db, post_id=post_dict["id"])
        update_post_likes_count(db, post_id=post_dict["id"])
        update_post_comments_count(db, post_id=post_dict["id"])


def activate_comments_by_owner_id(db: Session, owner_id: int):
    (
        db.query(models.Comment)
        .filter(models.Comment.owner_id == owner_id)
        .update({models.Comment.is_owner_active: True})
    )

    comments = (
        db.query(models.Comment)
        .filter(models.Comment.owner_id == owner_id)
        .all()
    )

    for comment in comments:
        comment_dict = comment.__dict__
        activate_like_comment_owner_by_comment_id(
            db, comment_id=comment_dict["id"]
        )
        update_comment_likes_count(db, comment_id=comment_dict["id"])
        update_post_comments_count(db, post_id=comment_dict["post_id"])


def activate_likes_by_owner_id(db: Session, owner_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.owner_id == owner_id)
        .update({models.Like.is_owner_active: True})
    )

    likes = (
        db.query(models.Like)
        .filter(models.Like.owner_id == owner_id)
        .all()
    )

    for like in likes:
        like_dict = like.__dict__

        if like_dict["post_id"]:
            update_post_likes_count(db, post_id=like_dict["post_id"])
        else:
            update_comment_likes_count(db, comment_id=like_dict["comment_id"])


def activate_followers_by_user_id(db: Session, user_id: int):
    (
        db.query(models.Follow)
        .filter(models.Follow.following_id == user_id)
        .update({models.Follow.is_following_active: True})
    )

    followers = (
        db.query(models.Follow)
        .filter(models.Follow.following_id == user_id)
        .all()
    )

    for follower in followers:
        update_user_followings_count(
            db, user_id=follower.__dict__["follower_id"]
        )


def activate_followings_by_user_id(db: Session, user_id: int):
    (
        db.query(models.Follow)
        .filter(models.Follow.follower_id == user_id)
        .update({models.Follow.is_follower_active: True})
    )

    followings = (
        db.query(models.Follow)
        .filter(models.Follow.following_id == user_id)
        .all()
    )

    for following in followings:
        update_user_followers_count(
            db, user_id=following.__dict__["follower_id"]
        )


def activate_likes_by_post_id(db: Session, post_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.post_id == post_id)
        .update({models.Like.is_post_active: True})
    )


def activate_likes_by_comment_id(db: Session, comment_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.comment_id == comment_id)
        .update({models.Like.is_comment_active: True})
    )


def activate_like_post_owner_by_post_id(db: Session, post_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.post_id == post_id)
        .update({models.Like.is_post_owner_active: True})
    )


def activate_like_comment_owner_by_comment_id(db: Session, comment_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.comment_id == comment_id)
        .update({models.Like.is_comment_owner_active: True})
    )


def deactivate_posts_by_owner_id(db: Session, owner_id: int):
    posts = (
        db.query(models.Post)
        .filter(models.Post.owner_id == owner_id)
        .all()
    )

    for post in posts:
        deactivate_likes_post_owner_by_post_id(db, post_id=post.__dict__["id"])

    (
        db.query(models.Post)
        .filter(models.Post.owner_id == owner_id)
        .update({models.Post.is_owner_active: False})
    )


def deactivate_comments_by_owner_id(db: Session, owner_id: int):
    (
        db.query(models.Comment)
        .filter(models.Comment.owner_id == owner_id)
        .update({models.Comment.is_owner_active: False})
    )

    comments = (
        db.query(models.Comment)
        .filter(models.Comment.owner_id == owner_id)
        .all()
    )

    for comment in comments:
        comment_dict = comment.__dict__

        deactivate_likes_comment_owner_by_comment_id(
            db, comment_id=comment_dict["id"]
        )
        update_post_comments_count(db, post_id=comment_dict["post_id"])


def deactivate_likes_by_owner_id(db: Session, owner_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.owner_id == owner_id)
        .update({models.Like.is_owner_active: False})
    )

    likes = (
        db.query(models.Like)
        .filter(models.Like.owner_id == owner_id)
        .all()
    )

    for like in likes:
        like_dict = like.__dict__

        if like_dict["post_id"]:
            update_post_likes_count(db, post_id=like_dict["post_id"])
        else:
            update_comment_likes_count(db, comment_id=like_dict["comment_id"])


def deactivate_followers_by_user_id(db: Session, user_id: int):
    (
        db.query(models.Follow)
        .filter(models.Follow.following_id == user_id)
        .update({models.Follow.is_following_active: False})
    )

    followers = (
        db.query(models.Follow)
        .filter(models.Follow.following_id == user_id)
        .all()
    )

    for follower in followers:
        update_user_followings_count(
            db, user_id=follower.__dict__["follower_id"]
        )


def deactivate_followings_by_user_id(db: Session, user_id: int):
    (
        db.query(models.Follow)
        .filter(models.Follow.follower_id == user_id)
        .update({models.Follow.is_follower_active: False})
    )

    followings = (
        db.query(models.Follow)
        .filter(models.Follow.follower_id == user_id)
        .all()
    )

    for following in followings:
        update_user_followers_count(
            db, user_id=following.__dict__["following_id"]
        )


def deactivate_likes_by_post_id(db: Session, post_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.post_id == post_id)
        .update({models.Like.is_post_active: False})
    )


def deactivate_likes_by_comment_id(db: Session, comment_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.comment_id == comment_id)
        .update({models.Like.is_comment_active: False})
    )


def deactivate_likes_post_owner_by_post_id(db: Session, post_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.post_id == post_id)
        .update({models.Like.is_post_owner_active: False})
    )


def deactivate_likes_comment_owner_by_comment_id(db: Session, comment_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.comment_id == comment_id)
        .update({models.Like.is_comment_owner_active: False})
    )


def update_user_posts_count(db: Session, owner_id: int):
    count = (
        db.query(models.Post)
        .filter(models.Post.is_active == True, models.Post.is_owner_active == True)
        .filter(models.Post.owner_id == owner_id)
        .count()
    )

    (
        db.query(models.User)
        .filter(models.User.id == owner_id)
        .update({models.User.posts: count})
    )


def update_post_comments_count(db: Session, post_id: int):
    count = (
        db.query(models.Comment)
        .filter(models.Comment.is_active == True, models.Comment.is_owner_active == True)
        .filter(models.Comment.post_id == post_id)
        .count()
    )

    (
        db.query(models.Post)
        .filter(models.Post.id == post_id)
        .update({models.Post.comments: count})
    )


def update_post_likes_count(db: Session, post_id: int):
    count = (
        db.query(models.Like)
        .filter(models.Like.is_comment_active == True, models.Like.is_post_active == True, models.Like.is_owner_active == True)
        .filter(models.Like.post_id == post_id)
        .count()
    )

    (
        db.query(models.Post)
        .filter(models.Post.id == post_id)
        .update({models.Post.likes: count})
    )


def update_comment_likes_count(db: Session, comment_id: int):
    count = (
        db.query(models.Like)
        .filter(models.Like.is_comment_active == True, models.Like.is_post_active == True, models.Like.is_owner_active == True)
        .filter(models.Like.comment_id == comment_id)
        .count()
    )

    (
        db.query(models.Comment)
        .filter(models.Comment.id == comment_id)
        .update({models.Comment.likes: count})
    )


def update_user_followers_count(db: Session, user_id: int):
    count = (
        db.query(models.Follow)
        .filter(models.Follow.is_follower_active == True, models.Follow.is_following_active == True)
        .filter(models.Follow.following_id == user_id)
        .count()
    )

    (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .update({models.User.followers: count})
    )


def update_user_followings_count(db: Session, user_id: int):
    count = (
        db.query(models.Follow)
        .filter(models.Follow.is_follower_active == True, models.Follow.is_following_active == True)
        .filter(models.Follow.follower_id == user_id)
        .count()
    )

    (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .update({models.User.followings: count})
    )
