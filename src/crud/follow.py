from sqlalchemy.orm import Session
from src import models


class Follow():
    def follow(self, db: Session, follower_id: int, following_id: int) -> models.Follow:
        db_follow = models.Follow(
            follower_id=follower_id,
            following_id=following_id,
        )
        db.add(db_follow)
        db.commit()

        self.update_followers_count(db, user_id=following_id)
        self.update_followings_count(db, user_id=follower_id)

        db.refresh(db_follow)
        return db_follow

    def unfollow(self, db: Session, follower_id: int, following_id: int) -> models.Follow:
        db_follow = self.get_follow(
            db, follower_id=follower_id, following_id=following_id
        )
        db.delete(db_follow)
        db.commit()

        self.update_followers_count(db, user_id=following_id)
        self.update_followings_count(db, user_id=follower_id)

        return db_follow

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[models.Follow]:
        return (
            db.query(models.Follow)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, db: Session, id: int) -> models.Follow | None:
        return (
            db.query(models.Follow)
            .filter(models.Follow.id == id)
            .first()
        )

    def get_follow(self, db: Session, follower_id: int, following_id: int) -> models.Follow | None:
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

    def update_followings_count(self, db: Session, user_id: int):
        db_user = (
            db.query(models.User)
            .filter(models.User.id == user_id)
            .first()
        )
        count = self.get_followings_count_by_user_id(db, user_id=user_id)

        setattr(db_user, "followings", count)

        db.commit()
        db.refresh(db_user)

    def update_followers_count(self, db: Session, user_id: int):
        db_user = (
            db.query(models.User)
            .filter(models.User.id == user_id)
            .first()
        )
        count = self.get_followers_count_by_user_id(db, user_id=user_id)

        setattr(db_user, "followers", count)

        db.commit()
        db.refresh(db_user)


follow = Follow()
