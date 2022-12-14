from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from src import models, schemas
from src.crud.utils import utils


class Post():
    def create(self, db: Session, post: schemas.PostCreate, owner_id: int) -> models.Post:
        db_post = models.Post(
            **post.dict(),
            owner_id=owner_id,
        )
        db.add(db_post)
        db.commit()

        utils.update_user_posts_count(db, owner_id=owner_id)
        db.commit()

        db.refresh(db_post)
        return db_post

    def update(self, db: Session, id: int, post_update: schemas.PostUpdate) -> models.Post:
        db_post = self.get_post_by_id(db, id=id)

        update_data = post_update.dict(exclude_unset=True)
        update_data["is_modified"] = True
        update_data["modified_at"] = func.now()

        for field, value in update_data.items():
            setattr(db_post, field, value)

        db.commit()
        db.refresh(db_post)
        return db_post

    def delete(self, db: Session, id: int):
        db_post = self.get_post_by_id(db, id=id)
        db.delete(db_post)
        db.commit()

        utils.delete_likes_by_post_id(db, post_id=id)
        utils.update_user_posts_count(
            db, owner_id=getattr(db_post, "owner_id")
        )
        db.commit()

    def activate(self, db: Session, id: int) -> models.Post:
        db_post = self.get_post_by_id(db, id=id)
        setattr(db_post, "is_active", True)
        db.commit()

        utils.activate_likes_by_post_id(db, post_id=id)
        utils.update_post_likes_count(db, post_id=id)
        utils.update_post_comments_count(db, post_id=id)
        utils.update_user_posts_count(
            db, owner_id=getattr(db_post, "owner_id")
        )

        db.commit()
        db.refresh(db_post)
        return db_post

    def deactivate(self, db: Session, id: int) -> models.Post:
        db_post = self.get_post_by_id(db, id=id)
        setattr(db_post, "is_active", False)
        db.commit()

        utils.deactivate_likes_by_post_id(db, post_id=id)
        utils.update_user_posts_count(
            db, owner_id=getattr(db_post, "owner_id")
        )

        db.commit()
        db.refresh(db_post)
        return db_post

    def get_post_by_id(self, db: Session, id: int) -> models.Post | None:
        return (
            db.query(models.Post)
            .filter(models.Post.id == id)
            .first()
        )

    def get_all_posts_count(self, db: Session) -> int:
        return (
            db.query(models.Post)
            .count()
        )

    def get_all_posts(self, db: Session, skip: int = 0, limit: int = 100) -> list[models.Post]:
        return (
            db.query(models.Post)
            .order_by(models.Post.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_posts_count_by_owner_id(self, db: Session, owner_id: int) -> int:
        return (
            db.query(models.Post)
            .filter(models.Post.owner_id == owner_id)
            .count()
        )

    def get_posts_by_owner_id(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> list[models.Post]:
        return (
            db.query(models.Post)
            .filter(models.Post.owner_id == owner_id)
            .order_by(models.Post.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_post_by_id(self, db: Session, id: int) -> models.Post | None:
        return (
            db.query(models.Post)
            .filter(models.Post.is_active == True, models.Post.is_owner_active == True)
            .filter(models.Post.id == id)
            .first()
        )

    def get_all_active_posts_count(self, db: Session) -> int:
        return (
            db.query(models.Post)
            .filter(models.Post.is_active == True, models.Post.is_owner_active == True)
            .count()
        )

    def get_all_active_posts(self, db: Session, skip: int = 0, limit: int = 100) -> list[models.Post]:
        return (
            db.query(models.Post)
            .filter(models.Post.is_active == True, models.Post.is_owner_active == True)
            .order_by(models.Post.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_posts_count_by_owner_id(self, db: Session, owner_id: int) -> int:
        return (
            db.query(models.Post)
            .filter(models.Post.is_active == True, models.Post.is_owner_active == True)
            .filter(models.Post.owner_id == owner_id)
            .count()
        )

    def get_active_posts_by_owner_id(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> list[models.Post]:
        return (
            db.query(models.Post)
            .filter(models.Post.is_active == True, models.Post.is_owner_active == True)
            .filter(models.Post.owner_id == owner_id)
            .order_by(models.Post.id)
            .offset(skip)
            .limit(limit)
            .all()
        )


post = Post()
