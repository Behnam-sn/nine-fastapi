from sqlalchemy import select
from sqlalchemy.orm import Session
from src import models


def activate_user_posts(db: Session, owner_id: int):
    query = (
        db.query(models.Post)
        .filter(models.Post.owner_id == owner_id)
        .all()
    )

    for post in query:
        activate_like_post_owner(db, post_id=post.__dict__["id"])

    (
        db.query(models.Post)
        .filter(models.Post.owner_id == owner_id)
        .update({models.Post.is_owner_active: True})
    )


def deactivate_user_posts(db: Session, owner_id: int):
    query = (
        db.query(models.Post)
        .filter(models.Post.owner_id == owner_id)
        .all()
    )

    for post in query:
        deactivate_like_post_owner(db, post_id=post.__dict__["id"])

    (
        db.query(models.Post)
        .filter(models.Post.owner_id == owner_id)
        .update({models.Post.is_owner_active: False})
    )


def activate_user_comments(db: Session, owner_id: int):
    query = (
        db.query(models.Comment)
        .filter(models.Comment.owner_id == owner_id)
        .all()
    )

    for comment in query:
        activate_like_comment_owner(db, comment_id=comment.__dict__["id"])

    (
        db.query(models.Comment)
        .filter(models.Comment.owner_id == owner_id)
        .update({models.Comment.is_owner_active: True})
    )


def deactivate_user_comments(db: Session, owner_id: int):
    query = (
        db.query(models.Comment)
        .filter(models.Comment.owner_id == owner_id)
        .all()
    )

    for comment in query:
        deactivate_like_comment_owner(db, comment_id=comment.__dict__["id"])

    (
        db.query(models.Comment)
        .filter(models.Comment.owner_id == owner_id)
        .update({models.Comment.is_owner_active: False})
    )


def activate_user_likes(db: Session, owner_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.owner_id == owner_id)
        .update({models.Like.is_owner_active: True})
    )

    query = (
        db.query(models.Like)
        .filter(models.Like.owner_id == owner_id)
        .all()
    )

    for like in query:
        like_dict = like.__dict__

        if like_dict["post_id"]:
            update_post_likes_count(db, post_id=like_dict["post_id"])
        else:
            update_comment_likes_count(db, comment_id=like_dict["comment_id"])


def deactivate_user_likes(db: Session, owner_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.owner_id == owner_id)
        .update({models.Like.is_owner_active: False})
    )

    query = (
        db.query(models.Like)
        .filter(models.Like.owner_id == owner_id)
        .all()
    )

    for like in query:
        like_dict = like.__dict__

        if like_dict["post_id"]:
            update_post_likes_count(db, post_id=like_dict["post_id"])
        else:
            update_comment_likes_count(db, comment_id=like_dict["comment_id"])


def activate_user_followers(db: Session, user_id: int):
    (
        db.query(models.Follow)
        .filter(models.Follow.following_id == user_id)
        .update({models.Follow.is_following_active: True})
    )


def deactivate_user_followers(db: Session, user_id: int):
    (
        db.query(models.Follow)
        .filter(models.Follow.following_id == user_id)
        .update({models.Follow.is_following_active: False})
    )


def activate_user_followings(db: Session, user_id: int):
    (
        db.query(models.Follow)
        .filter(models.Follow.follower_id == user_id)
        .update({models.Follow.is_follower_active: True})
    )


def deactivate_user_followings(db: Session, user_id: int):
    (
        db.query(models.Follow)
        .filter(models.Follow.follower_id == user_id)
        .update({models.Follow.is_follower_active: False})
    )


def activate_post_likes(db: Session, post_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.post_id == post_id)
        .update({models.Like.is_post_active: True})
    )


def deactivate_post_likes(db: Session, post_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.post_id == post_id)
        .update({models.Like.is_post_active: False})
    )


def activate_comment_likes(db: Session, comment_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.comment_id == comment_id)
        .update({models.Like.is_comment_active: True})
    )


def deactivate_comment_likes(db: Session, comment_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.comment_id == comment_id)
        .update({models.Like.is_comment_active: False})
    )


def activate_like_post_owner(db: Session, post_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.post_id == post_id)
        .update({models.Like.is_post_owner_active: True})
    )


def deactivate_like_post_owner(db: Session, post_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.post_id == post_id)
        .update({models.Like.is_post_owner_active: False})
    )


def activate_like_comment_owner(db: Session, comment_id: int):
    (
        db.query(models.Like)
        .filter(models.Like.comment_id == comment_id)
        .update({models.Like.is_comment_owner_active: True})
    )


def deactivate_like_comment_owner(db: Session, comment_id: int):
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
