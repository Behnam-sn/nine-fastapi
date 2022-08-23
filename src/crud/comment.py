from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from src import models, schemas


class Comment():
    def create(self, db: Session, comment: schemas.CommentCreate, owner_id: int) -> models.Comment:
        db_comment = models.Comment(
            **comment.dict(),
            owner_id=owner_id,
        )
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    def get_count(self, db: Session) -> int:
        return db.query(models.Comment).count()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[models.Comment]:
        return (
            db.query(models.Comment)
            .order_by(models.Comment.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, db: Session, id: int) -> models.Comment | None:
        return (
            db.query(models.Comment)
            .filter(models.Comment.id == id)
            .first()
        )

    def get_count_by_owner_id(self, db: Session, owner_id: int) -> int:
        return db.query(models.Post).filter(models.Comment.owner_id == owner_id).count()

    def get_by_owner_id(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> list[models.Comment]:
        return (
            db.query(models.Comment)
            .filter(models.Comment.owner_id == owner_id)
            .order_by(models.Comment.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_count_by_post_id(self, db: Session, post_id: int) -> int:
        return db.query(models.Post).filter(models.Comment.post_id == post_id).count()

    def get_by_post_id(self, db: Session, post_id: int, skip: int = 0, limit: int = 100) -> list[models.Comment]:
        return (
            db.query(models.Comment)
            .filter(models.Comment.post_id == post_id)
            .order_by(models.Comment.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(self, db: Session, id: int, comment_update: schemas.CommentUpdate) -> models.Comment:
        db_comment = self.get_by_id(db, id=id)

        update_data = comment_update.dict(exclude_unset=True)
        update_data["is_edited"] = True
        update_data["modified_at"] = func.now()

        for field, value in update_data.items():
            setattr(db_comment, field, value)

        db.commit()
        db.refresh(db_comment)
        return db_comment

    def delete(self, db: Session, id: int) -> models.Comment:
        db_comment = self.get_by_id(db, id=id)
        db.delete(db_comment)
        db.commit()
        return db_comment

    def active(self, db: Session, id: int) -> models.Comment:
        db_comment = self.get_by_id(db, id=id)
        setattr(db_comment, "is_active", True)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    def deactive(self, db: Session, id: int) -> models.Comment:
        db_comment = self.get_by_id(db, id=id)
        setattr(db_comment, "is_active", False)
        db.commit()
        db.refresh(db_comment)
        return db_comment


comment = Comment()
