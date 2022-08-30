from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.get("/all/", response_model=list[schemas.User])
def get_all_active_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
):
    return crud.user.get_all_active_users(db, skip=skip, limit=limit)


@router.get("/{username}", response_model=schemas.User)
def get_active_user_by_username(
    username: str,
    db: Session = Depends(deps.get_db),
):
    db_user = crud.user.get_active_user_by_username(db, username=username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@router.get("/count/", response_model=int)
def get_all_active_users_count(
    db: Session = Depends(deps.get_db),
):
    return crud.user.get_all_active_users_count(db)
