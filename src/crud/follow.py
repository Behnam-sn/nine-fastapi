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
        db.refresh(db_follow)
        return db_follow

    def unfollow(self, db: Session, follower_id: int, following_id: int) -> models.Follow:
        db_follow = self.get_follow(
            db, follower_id=follower_id, following_id=following_id
        )
        db.delete(db_follow)
        db.commit()
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

    def get_count_by_follower_id(self, db: Session, follower_id: int) -> int:
        return (
            db.query(models.Follow)
            .filter(models.Follow.follower_id == follower_id)
            .count()
        )

    def get_by_follower_id(self, db: Session, follower_id: int, skip: int = 0, limit: int = 100) -> list[models.Follow]:
        return (
            db.query(models.Follow)
            .filter(models.Follow.follower_id == follower_id)
            .order_by(models.Follow.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_count_by_following_id(self, db: Session, following_id: int) -> int:
        return (
            db.query(models.Follow)
            .filter(models.Follow.following_id == following_id)
            .count()
        )

    def get_by_following_id(self, db: Session, following_id: int, skip: int = 0, limit: int = 100) -> list[models.Follow]:
        return (
            db.query(models.Follow)
            .filter(models.Follow.following_id == following_id)
            .order_by(models.Follow.id)
            .offset(skip)
            .limit(limit)
            .all()
        )


follow = Follow()
