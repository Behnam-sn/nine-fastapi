from sqlalchemy.orm import Session
from src import models
from src.crud.utils import update_comment_likes_count, update_post_likes_count


class Like():
    def like_post(self, db: Session, post_id: int, owner_id: int) -> models.Like:
        db_like = models.Like(
            post_id=post_id,
            owner_id=owner_id,
        )
        db.add(db_like)
        db.commit()

        update_post_likes_count(db, post_id=post_id)
        db.commit()

        db.refresh(db_like)
        return db_like

    def unlike_post(self, db: Session, post_id: int, owner_id: int) -> models.Like:
        db_like = self.get_like_by_post_id_and_owner_id(
            db, post_id=post_id, owner_id=owner_id
        )
        db.delete(db_like)
        db.commit()

        update_post_likes_count(db, post_id=post_id)
        db.commit()

        return db_like

    def like_comment(self, db: Session, comment_id: int, owner_id: int) -> models.Like:
        db_like = models.Like(
            comment_id=comment_id,
            owner_id=owner_id,
        )
        db.add(db_like)
        db.commit()

        update_comment_likes_count(db, comment_id=comment_id)
        db.commit()

        db.refresh(db_like)
        return db_like

    def unlike_comment(self, db: Session, comment_id: int, owner_id: int) -> models.Like:
        db_like = self.get_like_by_comment_id_and_owner_id(
            db, comment_id=comment_id, owner_id=owner_id
        )
        db.delete(db_like)
        db.commit()

        update_comment_likes_count(db, comment_id=comment_id)
        db.commit()

        return db_like

    def get_like_by_post_id_and_owner_id(self, db: Session, post_id: int, owner_id: int) -> models.Like | None:
        return (
            db.query(models.Like)
            .filter(models.Like.post_id == post_id, models.Like.owner_id == owner_id)
            .first()
        )

    def get_like_by_comment_id_and_owner_id(self, db: Session, comment_id: int, owner_id: int) -> models.Like | None:
        return (
            db.query(models.Like)
            .filter(models.Like.comment_id == comment_id, models.Like.owner_id == owner_id)
            .first()
        )

    def get_like_by_id(self, db: Session, id: id) -> models.Like | None:
        return (
            db.query(models.Like)
            .filter(models.Like.id == id)
            .first()
        )

    def get_all_likes_count(self, db: Session):
        return (
            db.query(models.Like)
            .count()
        )

    def get_all_likes(self, db: Session, skip: int = 0, limit: int = 100) -> list[models.Like]:
        return (
            db.query(models.Like)
            .order_by(models.Like.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_likes_count_by_owner_id(self, db: Session, owner_id: int) -> int:
        return (
            db.query(models.Like)
            .filter(models.Like.owner_id == owner_id)
            .count()
        )

    def get_likes_by_owner_id(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> list[models.Like]:
        return (
            db.query(models.Like)
            .filter(models.Like.owner_id == owner_id)
            .order_by(models.Like.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_likes_count_by_post_id(self, db: Session, post_id: int) -> int:
        return (
            db.query(models.Like)
            .filter(models.Like.post_id == post_id)
            .count()
        )

    def get_likes_by_post_id(self, db: Session, post_id: int, skip: int = 0, limit: int = 100) -> list[models.Like]:
        return (
            db.query(models.Like)
            .filter(models.Like.post_id == post_id)
            .order_by(models.Like.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_likes_count_by_comment_id(self, db: Session, comment_id: int) -> int:
        return (
            db.query(models.Like)
            .filter(models.Like.comment_id == comment_id)
            .count()
        )

    def get_likes_by_comment_id(self, db: Session, comment_id: int, skip: int = 0, limit: int = 100) -> list[models.Like]:
        return (
            db.query(models.Like)
            .filter(models.Like.comment_id == comment_id)
            .order_by(models.Like.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_like_by_id(self, db: Session, id: id) -> models.Like | None:
        return (
            db.query(models.Like)
            .filter(models.Like.is_comment_active == True, models.Like.is_post_active == True, models.Like.is_owner_active == True)
            .filter(models.Like.id == id)
            .first()
        )

    def get_all_active_likes_count(self, db: Session):
        return (
            db.query(models.Like)
            .filter(models.Like.is_comment_active == True, models.Like.is_post_active == True, models.Like.is_owner_active == True)
            .count()
        )

    def get_all_active_likes(self, db: Session, skip: int = 0, limit: int = 100) -> list[models.Like]:
        return (
            db.query(models.Like)
            .filter(models.Like.is_comment_active == True, models.Like.is_post_active == True, models.Like.is_owner_active == True)
            .order_by(models.Like.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_likes_count_by_owner_id(self, db: Session, owner_id: int) -> int:
        return (
            db.query(models.Like)
            .filter(models.Like.is_comment_active == True, models.Like.is_post_active == True, models.Like.is_owner_active == True)
            .filter(models.Like.owner_id == owner_id)
            .count()
        )

    def get_active_likes_by_owner_id(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> list[models.Like]:
        return (
            db.query(models.Like)
            .filter(models.Like.is_comment_active == True, models.Like.is_post_active == True, models.Like.is_owner_active == True)
            .filter(models.Like.owner_id == owner_id)
            .order_by(models.Like.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_likes_count_by_post_id(self, db: Session, post_id: int) -> int:
        return (
            db.query(models.Like)
            .filter(models.Like.is_comment_active == True, models.Like.is_post_active == True, models.Like.is_owner_active == True)
            .filter(models.Like.post_id == post_id)
            .count()
        )

    def get_active_likes_by_post_id(self, db: Session, post_id: int, skip: int = 0, limit: int = 100) -> list[models.Like]:
        return (
            db.query(models.Like)
            .filter(models.Like.is_comment_active == True, models.Like.is_post_active == True, models.Like.is_owner_active == True)
            .filter(models.Like.post_id == post_id)
            .order_by(models.Like.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_likes_count_by_comment_id(self, db: Session, comment_id: int) -> int:
        return (
            db.query(models.Like)
            .filter(models.Like.is_comment_active == True, models.Like.is_post_active == True, models.Like.is_owner_active == True)
            .filter(models.Like.comment_id == comment_id)
            .count()
        )

    def get_active_likes_by_comment_id(self, db: Session, comment_id: int, skip: int = 0, limit: int = 100) -> list[models.Like]:
        return (
            db.query(models.Like)
            .filter(models.Like.is_comment_active == True, models.Like.is_post_active == True, models.Like.is_owner_active == True)
            .filter(models.Like.comment_id == comment_id)
            .order_by(models.Like.id)
            .offset(skip)
            .limit(limit)
            .all()
        )


like = Like()
