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

        self.update_post_count(db, post_id=getattr(db_comment, "post_id"))
        self.update_owner_count(db, owner_id=owner_id)

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

        self.update_post_count(db, post_id=getattr(db_comment, "post_id"))
        self.update_owner_count(db, owner_id=getattr(db_comment, "owner_id"))

    def active(self, db: Session, id: int) -> models.Comment:
        db_comment = self.get_by_id(db, id=id)
        setattr(db_comment, "is_active", True)
        db.commit()

        self.update_post_count(db, post_id=getattr(db_comment, "post_id"))
        self.update_owner_count(db, owner_id=getattr(db_comment, "owner_id"))

        db.refresh(db_comment)
        return db_comment

    def deactive(self, db: Session, id: int) -> models.Comment:
        db_comment = self.get_by_id(db, id=id)
        setattr(db_comment, "is_active", False)
        db.commit()

        self.update_post_count(db, post_id=getattr(db_comment, "post_id"))
        self.update_owner_count(db, owner_id=getattr(db_comment, "owner_id"))

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
            .filter(models.Comment.is_active == True)
            .count()
        )

    def get_all_active_comments(self, db: Session, skip: int = 0, limit: int = 100) -> list[models.Comment]:
        return (
            db.query(models.Comment)
            .filter(models.Comment.is_active == True)
            .order_by(models.Comment.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_comments_count_by_owner_id(self, db: Session, owner_id: int) -> int:
        return (
            db.query(models.Comment)
            .filter(models.Comment.owner_id == owner_id, models.Comment.is_active == True)
            .count()
        )

    def get_active_comments_by_owner_id(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> list[models.Comment]:
        return (
            db.query(models.Comment)
            .filter(models.Comment.owner_id == owner_id, models.Comment.is_active == True)
            .order_by(models.Comment.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_comments_count_by_post_id(self, db: Session, post_id: int) -> int:
        return (
            db.query(models.Comment)
            .filter(models.Comment.post_id == post_id, models.Comment.is_active == True)
            .count()
        )

    def get_active_comments_by_post_id(self, db: Session, post_id: int, skip: int = 0, limit: int = 100) -> list[models.Comment]:
        return (
            db.query(models.Comment)
            .filter(models.Comment.post_id == post_id, models.Comment.is_active == True)
            .order_by(models.Comment.id)
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
        count = self.get_active_comments_count_by_owner_id(
            db, owner_id=owner_id)

        setattr(db_user, "comments", count)

        db.commit()
        db.refresh(db_user)

    def update_post_count(self, db: Session, post_id: int):
        db_post = (
            db.query(models.Post)
            .filter(models.Post.id == post_id)
            .first()
        )
        count = self.get_active_comments_count_by_post_id(db, post_id=post_id)

        setattr(db_post, "comments", count)

        db.commit()
        db.refresh(db_post)


comment = Comment()
