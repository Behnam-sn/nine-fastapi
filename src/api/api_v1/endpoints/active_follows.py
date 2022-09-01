from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.get("/all/", response_model=list[schemas.Follow])
def get_all_active_follows(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):
    return crud.follow.get_all_active_follows(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.Follow)
def get_active_follow_by_id(
    id: int,
    db: Session = Depends(deps.get_db),
):
    db_follow = crud.follow.get_active_follow_by_id(db, id=id)

    if db_follow is None:
        raise HTTPException(status_code=404, detail="Follow not found")

    return db_follow


@router.get("/count/", response_model=int)
def get_all_active_follows_count(
    db: Session = Depends(deps.get_db)
):
    return crud.follow.get_all_active_follows_count(db)


@router.get("/following/count/{user_id}", response_model=int)
def get_active_following_count_by_user_id(
    user_id: int,
    db: Session = Depends(deps.get_db)
):
    db_user = crud.user.get_active_user_by_id(db, id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.follow.get_active_followings_count_by_user_id(db, user_id=user_id)


@router.get("/following/ids/{user_id}", response_model=list[schemas.Id])
def get_active_following_ids_by_user_id(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
):
    db_user = crud.user.get_active_user_by_id(db, id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.follow.get_active_followings_by_user_id(db, user_id=user_id, skip=skip, limit=limit)


@router.get("/follower/count/{user_id}", response_model=int)
def get_active_follower_count_by_user_id(
    user_id: int,
    db: Session = Depends(deps.get_db)
):
    db_user = crud.user.get_active_user_by_id(db, id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.follow.get_active_followers_count_by_user_id(db, user_id=user_id)


@router.get("/follower/ids/{user_id}", response_model=list[schemas.Id])
def get_active_follower_ids_by_user_id(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
):
    db_user = crud.user.get_active_user_by_id(db, id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.follow.get_active_followers_by_user_id(db, user_id=user_id, skip=skip, limit=limit)
