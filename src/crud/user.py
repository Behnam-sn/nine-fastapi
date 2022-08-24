from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from src import models, schemas
from src.core.security import get_password_hash, verify_password


class User():
    def create(self, db: Session, user: schemas.UserCreate) -> models.User:
        db_user = models.User(
            username=user.username,
            hashed_password=get_password_hash(user.password),
            name=user.name,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
        return (
            db.query(models.User)
            .order_by(models.User.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, db: Session, id: id) -> models.User | None:
        return (
            db.query(models.User)
            .filter(models.User.id == id)
            .first()
        )

    def get_by_username(self, db: Session, username: str) -> models.User | None:
        return (
            db.query(models.User)
            .filter(models.User.username == username)
            .first()
        )

    def update(self, db: Session, username: str, user_update: schemas.UserUpdate) -> models.User:
        db_user = self.get_by_username(db, username=username)

        update_data = user_update.dict(exclude_unset=True)
        update_data["modified_at"] = func.now()

        for field, value in update_data.items():
            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)
        return db_user

    def update_password(self, db: Session, username: str, new_password: str) -> models.User:
        db_user = self.get_by_username(db, username=username)

        hashed_password = get_password_hash(new_password)
        setattr(db_user, "hashed_password", hashed_password)
        setattr(db_user, "modified_at", func.now())

        db.commit()
        db.refresh(db_user)
        return db_user

    def activate(self, db: Session, username: str) -> models.User:
        db_user = self.get_by_username(db, username=username)
        setattr(db_user, "is_active", True)
        db.commit()
        db.refresh(db_user)
        return db_user

    def deactivate(self, db: Session, username: str) -> models.User:
        db_user = self.get_by_username(db, username=username)
        setattr(db_user, "is_active", False)
        db.commit()
        db.refresh(db_user)
        return db_user

    def authenticate(self, db: Session, username: str, password: str) -> models.User | None:
        db_user = self.get_by_username(db, username=username)

        if not db_user:
            return None

        if not verify_password(password, db_user.hashed_password):
            return None

        return db_user


user = User()
