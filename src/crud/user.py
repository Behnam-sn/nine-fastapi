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


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user(db: Session, username: str, user_update: schemas.UserUpdate) -> models.User:
    db_user = get_user_by_username(db, username=username)
    update_data = user_update.dict(exclude_unset=True)

    if db_user.username != update_data["username"]:
        # db_notes = db.query(models.Note).filter(
        #     models.Note.author == username
        # ).all()

        # for note in db_notes:
        #     setattr(note, "author", update_data["username"])

        setattr(db_user, "username", update_data["username"])

    if db_user.name != update_data["name"]:
        setattr(db_user, "name", update_data["name"])

    if db_user.bio != update_data["bio"]:
        setattr(db_user, "bio", update_data["bio"])

    setattr(db_user, "modified_at", now())

    db.commit()
    db.refresh(db_user)
    return db_user


def update_password(db: Session, username: str, new_password: str) -> models.User:
    db_user = get_user_by_username(db, username=username)

    hashed_password = get_password_hash(new_password)
    setattr(db_user, "hashed_password", hashed_password)
    setattr(db_user, "modified_at", now())

    db.commit()
    db.refresh(db_user)
    return db_user


def activate_user(db: Session, username: str) -> models.User:
    db_user = get_user_by_username(db, username=username)
    setattr(db_user, "is_active", True)

    db.commit()
    db.refresh(db_user)
    return db_user


def deactivate_user(db: Session, username: str) -> models.User:
    db_user = get_user_by_username(db, username=username)
    setattr(db_user, "is_active", False)

    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str) -> models.User | None:
    db_user = get_user_by_username(db, username=username)

    if not db_user:
        return None

    if not verify_password(password, db_user.hashed_password):
        return None

    return db_user
