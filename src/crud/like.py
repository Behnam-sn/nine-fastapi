import datetime

from sqlalchemy.orm import Session
from src import models, schemas


def now():
    return datetime.datetime.now().strftime("%Y/%m/%d %H:%M")


class Like():
    def like_post(self, db: Session, post_id: int, owner_id: int) -> models.Like:
        db_like = models.Like(
            post_id=post_id,
            owner_id=owner_id,
            created_at=now(),
        )
        db.add(db_like)
        db.commit()
        db.refresh(db_like)
        return db_like

    def like_comment(self, db: Session, comment_id: int, owner_id: int) -> models.Like:
        db_like = models.Like(
            comment_id=comment_id,
            owner_id=owner_id,
            created_at=now(),
        )
        db.add(db_like)
        db.commit()
        db.refresh(db_like)
        return db_like

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[models.Like]:
        return (
            db.query(models.Like)
            .order_by(models.Like.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_post_like(self, db: Session, post_id: int, owner_id: int) -> models.Like | None:
        return (
            db.query(models.Like)
            .filter(models.Like.post_id == post_id, models.Like.owner_id == owner_id)
            .first()
        )

    def get_comment_like(self, db: Session, comment_id: int, owner_id: int) -> models.Like | None:
        return (
            db.query(models.Like)
            .filter(models.Like.comment_id == comment_id, models.Like.owner_id == owner_id)
            .first()
        )

    def unlike_post(self, db: Session, post_id: int, owner_id: int) -> models.Like:
        db_like = self.get_post_like(db, post_id=post_id, owner_id=owner_id)
        db.delete(db_like)
        db.commit()
        return db_like

    def unlike_comment(self, db: Session, comment_id: int, owner_id: int) -> models.Like:
        db_like = self.get_comment_like(
            db, comment_id=comment_id, owner_id=owner_id
        )
        db.delete(db_like)
        db.commit()
        return db_like


like = Like()
