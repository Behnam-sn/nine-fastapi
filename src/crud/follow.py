import datetime

from sqlalchemy.orm import Session
from src import models


def now():
    return datetime.datetime.now().strftime("%Y/%m/%d %H:%M")


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

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[models.Follow]:
        return (
            db.query(models.Follow)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_follow(self, db: Session, follower_id: int, following_id: int) -> models.Follow | None:
        return (
            db.query(models.Follow)
            .filter(models.Follow.follower_id == follower_id, models.Follow.following_id == following_id)
            .first()
        )

    def unfollow(self, db: Session, follower_id: int, following_id: int) -> models.Follow:
        db_follow = self.get_follow(
            db, follower_id=follower_id, following_id=following_id
        )
        db.delete(db_follow)
        db.commit()
        return db_follow


follow = Follow()
