from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api import deps
from src.core import security
from src.core.config import settings

router = APIRouter()


@router.post("/signup", response_model=schemas.Token)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(deps.get_db)
):

    if crud.user.get_user_by_username(db, username=user.username):
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )

    crud.user.create(db=db, user=user)

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = security.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signin", response_model=schemas.Token)
def sign_in(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(deps.get_db)
):

    user = crud.user.authenticate(
        db,
        username=form_data.username,
        password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(status_code=403, detail="user is not active",)

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = security.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# @router.post("/test-token", response_model=schemas.User)
# def test_token(
#     current_user: models.User = Depends(deps.get_current_user)
# ):
#     return current_user
