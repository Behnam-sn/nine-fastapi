import datetime

from sqlalchemy.orm import Session
from src import crud, models
from src.core.config import settings
from src.core.security import get_password_hash
from src.database import base  # keep


def now():
    return datetime.datetime.now().strftime("%Y/%m/%d %H:%M")


def init_db(db: Session):

    user = crud.user.get_by_username(db, username=settings.SUPERUSER_USERNAME)
    if not user:

        db_user = models.User(
            username=settings.SUPERUSER_USERNAME,
            hashed_password=get_password_hash(settings.SUPERUSER_PASSWORD),
            name="admin",
            is_superuser=True,
            created_at=now(),
            modified_at=now(),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
