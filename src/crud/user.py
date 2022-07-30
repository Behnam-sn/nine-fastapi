import datetime

from sqlalchemy.orm import Session
from src import models, schemas
from src.core.security import get_password_hash, verify_password


def now():
    return datetime.datetime.now().strftime("%Y/%m/%d %H:%M")


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        name=user.name,
        created_at=now(),
        modified_at=now(),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> models.User | None:
    db_user = get_user_by_username(db, username=username)

    if not db_user:
        return None

    if not verify_password(password, db_user.hashed_password):
        return None

    return db_user
