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

        self.update_owner_count(db, owner_id=owner_id)
        self.update_post_count(db, post_id=getattr(db_like, "post_id"))

        db.refresh(db_like)
        return db_like

    def unlike_post(self, db: Session, post_id: int, owner_id: int) -> models.Like:
        db_like = self.get_like_by_post_id_and_owner_id(
            db, post_id=post_id, owner_id=owner_id
        )
        db.delete(db_like)
        db.commit()

        self.update_owner_count(db, owner_id=owner_id)
        self.update_post_count(db, post_id=getattr(db_like, "post_id"))

        return db_like

    def like_comment(self, db: Session, comment_id: int, owner_id: int) -> models.Like:
        db_like = models.Like(
            comment_id=comment_id,
            owner_id=owner_id,
        )
        db.add(db_like)
        db.commit()

        self.update_owner_count(db, owner_id=owner_id)
        self.update_comment_count(
            db, comment_id=getattr(db_like, "comment_id")
        )

        db.refresh(db_like)
        return db_like

    def unlike_comment(self, db: Session, comment_id: int, owner_id: int) -> models.Like:
        db_like = self.get_like_by_comment_id_and_owner_id(
            db, comment_id=comment_id, owner_id=owner_id
        )
        db.delete(db_like)
        db.commit()

        self.update_owner_count(db, owner_id=owner_id)
        self.update_comment_count(
            db, comment_id=getattr(db_like, "comment_id")
        )

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

    def update_owner_count(self, db: Session, owner_id: int):
        db_user = (
            db.query(models.User)
            .filter(models.User.id == owner_id)
            .first()
        )
        count = self.get_likes_count_by_owner_id(db, owner_id=owner_id)

        setattr(db_user, "likes", count)

        db.commit()
        db.refresh(db_user)

    def update_post_count(self, db: Session, post_id: int):
        db_post = (
            db.query(models.Post)
            .filter(models.Post.id == post_id)
            .first()
        )
        count = self.get_likes_count_by_post_id(db, post_id=post_id)

        setattr(db_post, "likes", count)

        db.commit()
        db.refresh(db_post)

    def update_comment_count(self, db: Session, comment_id: int):
        db_commnet = (
            db.query(models.Comment)
            .filter(models.Comment.id == comment_id)
            .first()
        )
        count = self.get_likes_count_by_comment_id(db, comment_id=comment_id)

        setattr(db_commnet, "likes", count)

        db.commit()
        db.refresh(db_commnet)


like = Like()
