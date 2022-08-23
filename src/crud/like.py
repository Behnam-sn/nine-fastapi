from sqlalchemy.orm import Session
from src import models


class Like():
    def like_post(self, db: Session, post_id: int, owner_id: int) -> models.Like:
        db_like = models.Like(
            post_id=post_id,
            owner_id=owner_id,
        )
        db.add(db_like)
        db.commit()

    def unlike_post(self, db: Session, post_id: int, owner_id: int):
        db_like = self.get_post_by_owner_id(
            db, post_id=post_id, owner_id=owner_id)
        db.delete(db_like)
        db.commit()

    def like_comment(self, db: Session, comment_id: int, owner_id: int) -> models.Like:
        db_like = models.Like(
            comment_id=comment_id,
            owner_id=owner_id,
        )
        db.add(db_like)
        db.commit()

    def unlike_comment(self, db: Session, comment_id: int, owner_id: int):
        db_like = self.get_comment_by_owner_id(
            db, comment_id=comment_id, owner_id=owner_id
        )
        db.delete(db_like)
        db.commit()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[models.Like]:
        return (
            db.query(models.Like)
            .order_by(models.Like.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, db: Session, id: id) -> models.Like | None:
        return (
            db.query(models.Like)
            .filter(models.Like.id == id)
            .first()
        )

    def get_count_by_owner_id(self, db: Session, owner_id: int) -> int:
        return (
            db.query(models.Like)
            .filter(models.Like.owner_id == owner_id)
            .count()
        )

    def get_by_owner_id(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> list[models.Like]:
        return (
            db.query(models.Like)
            .filter(models.Like.owner_id == owner_id)
            .order_by(models.Like.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_post_by_owner_id(self, db: Session, post_id: int, owner_id: int) -> models.Like | None:
        return (
            db.query(models.Like)
            .filter(models.Like.post_id == post_id, models.Like.owner_id == owner_id)
            .first()
        )

    def get_count_by_post_id(self, db: Session, post_id: int) -> int:
        return (
            db.query(models.Like)
            .filter(models.Like.post_id == post_id)
            .count()
        )

    def get_by_post_id(self, db: Session, post_id: int, skip: int = 0, limit: int = 100) -> list[models.Like]:
        return (
            db.query(models.Like)
            .filter(models.Like.post_id == post_id)
            .order_by(models.Like.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_comment_by_owner_id(self, db: Session, comment_id: int, owner_id: int) -> models.Like | None:
        return (
            db.query(models.Like)
            .filter(models.Like.comment_id == comment_id, models.Like.owner_id == owner_id)
            .first()
        )

    def get_count_by_comment_id(self, db: Session, comment_id: int) -> int:
        return (
            db.query(models.Like)
            .filter(models.Like.comment_id == comment_id)
            .count()
        )

    def get_by_comment_id(self, db: Session, comment_id: int, skip: int = 0, limit: int = 100) -> list[models.Like]:
        return (
            db.query(models.Like)
            .filter(models.Like.comment_id == comment_id)
            .order_by(models.Like.id)
            .offset(skip)
            .limit(limit)
            .all()
        )


like = Like()
