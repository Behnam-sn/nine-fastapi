from sqlalchemy.orm import Session
from src import crud, models
from src.core.config import settings
from src.core.security import get_password_hash
from src.database import base  # keep


def init_db(db: Session):

    super_user = crud.user.get_user_by_username(
        db, username=settings.SUPERUSER_USERNAME
    )
    if not super_user:
        db_user = models.User(
            username=settings.SUPERUSER_USERNAME,
            hashed_password=get_password_hash(settings.SUPERUSER_PASSWORD),
            name="admin",
            is_superuser=True,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    normal_user = crud.user.get_user_by_username(
        db, username=settings.NORMAL_USERNAME
    )
    if not normal_user:
        db_user = models.User(
            username=settings.NORMAL_USERNAME,
            hashed_password=get_password_hash(settings.NORMAL_PASSWORD),
            name="a",
            is_superuser=False,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
