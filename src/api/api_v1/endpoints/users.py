from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.get("/current-user/", response_model=schemas.User)
def get_current_user(
    current_user: models.User = Depends(deps.get_current_user),
):
    return current_user


@router.get("/all/", response_model=list[schemas.User])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
):
    return crud.user.get_all_users(db, skip=skip, limit=limit)


@router.get("/{username}", response_model=schemas.User)
def get_user_by_username(
    username: str,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
):
    db_user = crud.user.get_user_by_username(db, username=username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@router.get("/count/", response_model=int)
def get_all_users_count(
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
):
    return crud.user.get_all_users_count(db)


@router.put("/", response_model=schemas.User)
def update_user(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    db_user = crud.user.get_active_user_by_username(
        db, username=current_user.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.username != user_update.username and crud.user.get_user_by_username(db, username=user_update.username):
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )

    return crud.user.update(db, username=current_user.username, user_update=user_update)


@router.delete("/{username}")
def delete_user(
    username: str,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db)
):
    db_user = crud.user.get_user_by_username(db, username=username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.user.delete(db, username=username)


@router.put("/activate/{username}", response_model=schemas.User)
def activate_user(
    username: str,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    db_user = crud.user.get_user_by_username(db, username=username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.is_superuser is False and current_user.username != username:
        raise HTTPException(status_code=401, detail="Not Authenticated")

    return crud.user.activate(db, username=username)


@router.put("/deactivate/{username}", response_model=schemas.User)
def deactivate_user(
    username: str,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    db_user = crud.user.get_active_user_by_username(db, username=username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.is_superuser is False and current_user.username != username:
        raise HTTPException(status_code=401, detail="Not Authenticated")

    return crud.user.deactivate(db, username=username)
