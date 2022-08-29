from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from src import models, schemas
from src.crud.utils import (activate_comment_likes, deactivate_comment_likes,
                            update_comment_likes_count,
                            update_post_comments_count)


class Comment():
    def create(self, db: Session, comment: schemas.CommentCreate, owner_id: int) -> models.Comment:
        db_comment = models.Comment(
            **comment.dict(),
            owner_id=owner_id,
        )
        db.add(db_comment)
        db.commit()

        update_post_comments_count(db, post_id=getattr(db_comment, "post_id"))

        db.refresh(db_comment)
        return db_comment

    def update(self, db: Session, id: int, comment_update: schemas.CommentUpdate) -> models.Comment:
        db_comment = self.get_by_id(db, id=id)

        update_data = comment_update.dict(exclude_unset=True)
        update_data["is_modified"] = True
        update_data["modified_at"] = func.now()

        for field, value in update_data.items():
            setattr(db_comment, field, value)

        db.commit()
        db.refresh(db_comment)
        return db_comment

    def delete(self, db: Session, id: int):
        db_comment = self.get_by_id(db, id=id)
        db.delete(db_comment)
        db.commit()

        update_post_comments_count(db, post_id=getattr(db_comment, "post_id"))

    def activate(self, db: Session, id: int) -> models.Comment:
        db_comment = self.get_by_id(db, id=id)
        setattr(db_comment, "is_active", True)
        db.commit()

        activate_comment_likes(db, comment_id=id)
        update_comment_likes_count(db, comment_id=id)
        update_post_comments_count(db, post_id=getattr(db_comment, "post_id"))

        db.refresh(db_comment)
        return db_comment

    def deactivate(self, db: Session, id: int) -> models.Comment:
        db_comment = self.get_by_id(db, id=id)
        setattr(db_comment, "is_active", False)
        db.commit()

        deactivate_comment_likes(db, comment_id=id)
        update_post_comments_count(db, post_id=getattr(db_comment, "post_id"))

        db.refresh(db_comment)
        return db_comment

    def get_by_id(self, db: Session, id: int) -> models.Comment | None:
        return (
            db.query(models.Comment)
            .filter(models.Comment.id == id)
            .first()
        )

    def get_all_active_comments_count(self, db: Session) -> int:
        return (
            db.query(models.Comment)
            .filter(models.Comment.is_active == True, models.Comment.is_owner_active == True)
            .count()
        )

    def get_all_active_comments(self, db: Session, skip: int = 0, limit: int = 100) -> list[models.Comment]:
        return (
            db.query(models.Comment)
            .filter(models.Comment.is_active == True, models.Comment.is_owner_active == True)
            .order_by(models.Comment.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_comments_count_by_owner_id(self, db: Session, owner_id: int) -> int:
        return (
            db.query(models.Comment)
            .filter(models.Comment.is_active == True, models.Comment.is_owner_active == True)
            .filter(models.Comment.owner_id == owner_id)
            .count()
        )

    def get_active_comments_by_owner_id(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> list[models.Comment]:
        return (
            db.query(models.Comment)
            .filter(models.Comment.is_active == True, models.Comment.is_owner_active == True)
            .filter(models.Comment.owner_id == owner_id)
            .order_by(models.Comment.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_comments_count_by_post_id(self, db: Session, post_id: int) -> int:
        return (
            db.query(models.Comment)
            .filter(models.Comment.is_active == True, models.Comment.is_owner_active == True)
            .filter(models.Comment.post_id == post_id)
            .count()
        )

    def get_active_comments_by_post_id(self, db: Session, post_id: int, skip: int = 0, limit: int = 100) -> list[models.Comment]:
        return (
            db.query(models.Comment)
            .filter(models.Comment.is_active == True, models.Comment.is_owner_active == True)
            .filter(models.Comment.post_id == post_id)
            .order_by(models.Comment.id)
            .offset(skip)
            .limit(limit)
            .all()
        )


comment = Comment()
