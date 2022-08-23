from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from src import models, schemas


class Post():
    def create(self, db: Session, post: schemas.PostCreate, owner_id: int) -> models.Post:
        db_post = models.Post(
            **post.dict(),
            owner_id=owner_id,
        )
        db.add(db_post)
        db.commit()

        self.update_count(db, owner_id=owner_id)

        db.refresh(db_post)
        return db_post

    def get_all_count(self, db: Session) -> int:
        return db.query(models.Post).count()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[models.Post]:
        return (
            db.query(models.Post)
            .order_by(models.Post.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, db: Session, id: int) -> models.Post | None:
        return (
            db.query(models.Post)
            .filter(models.Post.id == id)
            .first()
        )

    def get_count_by_owner_id(self, db: Session, owner_id: int) -> int:
        return (
            db.query(models.Post)
            .filter(models.Post.owner_id == owner_id, models.Post.is_active == True)
            .count()
        )

    def get_by_owner_id(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> list[models.Post]:
        return (
            db.query(models.Post)
            .filter(models.Post.owner_id == owner_id)
            .order_by(models.Post.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(self, db: Session, id: int, post_update: schemas.PostUpdate) -> models.Post:
        db_post = self.get_by_id(db, id=id)

        update_data = post_update.dict(exclude_unset=True)
        update_data["is_modified"] = True
        update_data["modified_at"] = func.now()

        for field, value in update_data.items():
            setattr(db_post, field, value)

        db.commit()
        db.refresh(db_post)
        return db_post

    def delete(self, db: Session, id: int):
        db_post = self.get_by_id(db, id=id)
        db.delete(db_post)
        db.commit()

        self.update_count(db, owner_id=getattr(db_post, "owner_id"))

    def active(self, db: Session, id: int) -> models.Post:
        db_post = self.get_by_id(db, id=id)
        setattr(db_post, "is_active", True)
        db.commit()

        self.update_count(db, owner_id=getattr(db_post, "owner_id"))

        db.refresh(db_post)
        return db_post

    def deactive(self, db: Session, id: int) -> models.Post:
        db_post = self.get_by_id(db, id=id)
        setattr(db_post, "is_active", False)
        db.commit()

        self.update_count(db, owner_id=getattr(db_post, "owner_id"))

        db.refresh(db_post)
        return db_post

    def update_count(self, db: Session, owner_id: int):
        db_user = (
            db.query(models.User)
            .filter(models.User.id == owner_id)
            .first()
        )
        count = self.get_count_by_owner_id(db, owner_id=owner_id)

        setattr(db_user, "posts", count)

        db.commit()
        db.refresh(db_user)


post = Post()
