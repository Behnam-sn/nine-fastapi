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
        db.refresh(db_post)
        return db_post

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[models.Post]:
        return (
            db.query(models.Post)
            .order_by(models.Post.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_length(self, db: Session) -> int:
        return db.query(models.Post).count()

    def get_by_id(self, db: Session, id: int) -> models.Post | None:
        return (
            db.query(models.Post)
            .filter(models.Post.id == id)
            .first()
        )

    def update(self, db: Session, id: int, post_update: schemas.PostUpdate) -> models.Post:
        db_post = self.get_by_id(db, id=id)

        update_data = post_update.dict(exclude_unset=True)
        update_data["is_edited"] = True
        update_data["modified_at"] = func.now()

        for field, value in update_data.items():
            setattr(db_post, field, value)

        db.commit()
        db.refresh(db_post)
        return db_post

    def delete(self, db: Session, id: int) -> models.Post:
        db_post = self.get_by_id(db, id=id)
        db.delete(db_post)
        db.commit()
        return db_post

    def active(self, db: Session, id: int) -> models.Post:
        db_post = self.get_by_id(db, id=id)
        setattr(db_post, "is_active", True)
        db.commit()
        db.refresh(db_post)
        return db_post

    def deactive(self, db: Session, id: int) -> models.Post:
        db_post = self.get_by_id(db, id=id)
        setattr(db_post, "is_active", False)
        db.commit()
        db.refresh(db_post)
        return db_post

    # def render_post_with_author(self, db: Session, post: models.Post) -> schemas.Post:
    #     author = db.query(models.User).filter(
    #         models.User.id == post.owner_id).first()

    #     return schemas.Post(
    #         id=post.id,
    #         text=post.text,
    #         author=schemas.Author(
    #             username=author.username,
    #             name=author.name,
    #         ),
    #         is_active=post.is_active,
    #         created_at=post.created_at,
    #         modified_at=post.modified_at,
    #     )


post = Post()
