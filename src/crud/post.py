import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session
from src import models, schemas


def now():
    return datetime.datetime.now().strftime("%Y/%m/%d %H:%M")


class Post():
    def create_post(self, db: Session, post: schemas.PostCreate, author_id: int) -> models.Post:
        db_post = models.Post(
            **post.dict(),
            author_id=author_id,
            created_at=now(),
            modified_at=now(),
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post

    def get_all_posts(self, db: Session, skip: int = 0, limit: int = 100) -> list[models.Post]:
        return (
            db.query(models.Post)
            .order_by(models.Post.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_post_by_id(self, db: Session, id: int) -> None | models.Post:
        return (
            db.query(models.Post)
            .filter(models.Post.id == id)
            .first()
        )

    def update_post(self, db: Session, id: int, post_update: schemas.PostUpdate) -> models.Post:
        db_post = self.get_post_by_id(db, id=id)

        update_data = post_update.dict(exclude_unset=True)
        update_data["modified_at"] = now()

        for field, value in update_data.items():
            setattr(db_post, field, value)

        db.commit()
        db.refresh(db_post)
        return db_post

    def render_post_with_author(self, db: Session, post: models.Post) -> schemas.Post:
        author = db.query(models.User).filter(
            models.User.id == post.author_id).first()

        return schemas.Post(
            id=post.id,
            text=post.text,
            author=schemas.UserInPost(
                username=author.username,
                name=author.name,
            ),
            is_active=post.is_active,
            created_at=post.created_at,
            modified_at=post.modified_at,
        )


post = Post()
