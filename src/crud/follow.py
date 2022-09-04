from sqlalchemy.orm import Session
from src import models
from src.crud.utils import (update_user_followers_count,
                            update_user_followings_count)


class Follow():
    def follow(self, db: Session, follower_id: int, following_id: int) -> models.Follow:
        db_follow = models.Follow(
            follower_id=follower_id,
            following_id=following_id,
        )
        db.add(db_follow)
        db.commit()

        update_user_followers_count(db, user_id=following_id)
        update_user_followings_count(db, user_id=follower_id)

        db.commit()
        db.refresh(db_follow)
        return db_follow

    def unfollow(self, db: Session, follower_id: int, following_id: int) -> models.Follow:
        db_follow = self.get_follow_by_follower_id_and_following_id(
            db, follower_id=follower_id, following_id=following_id
        )
        db.delete(db_follow)
        db.commit()

        update_user_followers_count(db, user_id=following_id)
        update_user_followings_count(db, user_id=follower_id)

        db.commit()
        return db_follow

    def get_all_follows_count(self, db: Session) -> int:
        return (
            db.query(models.Follow)
            .count()
        )

    def get_all_follows(self, db: Session, skip: int = 0, limit: int = 100) -> list[models.Follow]:
        return (
            db.query(models.Follow)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_follow_by_id(self, db: Session, id: int) -> models.Follow | None:
        return (
            db.query(models.Follow)
            .filter(models.Follow.id == id)
            .first()
        )

    def get_follow_by_follower_id_and_following_id(self, db: Session, follower_id: int, following_id: int) -> models.Follow | None:
        return (
            db.query(models.Follow)
            .filter(models.Follow.follower_id == follower_id, models.Follow.following_id == following_id)
            .first()
        )

    def get_followers_count_by_user_id(self, db: Session, user_id: int) -> int:
        return (
            db.query(models.Follow)
            .filter(models.Follow.following_id == user_id)
            .count()
        )

    def get_followers_by_user_id(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[models.Follow]:
        return (
            db.query(models.Follow)
            .filter(models.Follow.following_id == user_id)
            .order_by(models.Follow.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_followings_count_by_user_id(self, db: Session, user_id: int) -> int:
        return (
            db.query(models.Follow)
            .filter(models.Follow.follower_id == user_id)
            .count()
        )

    def get_followings_by_user_id(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[models.Follow]:
        return (
            db.query(models.Follow)
            .filter(models.Follow.follower_id == user_id)
            .order_by(models.Follow.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all_active_follows_count(self, db: Session) -> int:
        return (
            db.query(models.Follow)
            .filter(models.Follow.is_follower_active == True, models.Follow.is_following_active == True)
            .count()
        )

    def get_all_active_follows(self, db: Session, skip: int = 0, limit: int = 100) -> list[models.Follow]:
        return (
            db.query(models.Follow)
            .filter(models.Follow.is_follower_active == True, models.Follow.is_following_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_follow_by_id(self, db: Session, id: int) -> models.Follow | None:
        return (
            db.query(models.Follow)
            .filter(models.Follow.is_follower_active == True, models.Follow.is_following_active == True)
            .filter(models.Follow.id == id)
            .first()
        )

    # def get_active_follow_by_follower_id_and_following_id(self, db: Session, follower_id: int, following_id: int) -> models.Follow | None:
    #     return (
    #         db.query(models.Follow)
    #         .filter(models.Follow.is_follower_active == True, models.Follow.is_following_active == True)
    #         .filter(models.Follow.follower_id == follower_id, models.Follow.following_id == following_id)
    #         .first()
    #     )

    def get_active_followers_count_by_user_id(self, db: Session, user_id: int) -> int:
        return (
            db.query(models.Follow)
            .filter(models.Follow.is_follower_active == True, models.Follow.is_following_active == True)
            .filter(models.Follow.following_id == user_id)
            .count()
        )

    def get_active_followers_by_user_id(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[models.Follow]:
        return (
            db.query(models.Follow)
            .filter(models.Follow.is_follower_active == True, models.Follow.is_following_active == True)
            .filter(models.Follow.following_id == user_id)
            .order_by(models.Follow.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_followings_count_by_user_id(self, db: Session, user_id: int) -> int:
        return (
            db.query(models.Follow)
            .filter(models.Follow.is_follower_active == True, models.Follow.is_following_active == True)
            .filter(models.Follow.follower_id == user_id)
            .count()
        )

    def get_active_followings_by_user_id(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[models.Follow]:
        return (
            db.query(models.Follow)
            .filter(models.Follow.is_follower_active == True, models.Follow.is_following_active == True)
            .filter(models.Follow.follower_id == user_id)
            .order_by(models.Follow.id)
            .offset(skip)
            .limit(limit)
            .all()
        )


follow = Follow()
