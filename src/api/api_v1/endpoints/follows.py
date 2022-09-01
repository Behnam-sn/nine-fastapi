from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.get("/all/", response_model=list[schemas.Follow])
def get_all_follows(
    skip: int = 0,
    limit: int = 100,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db)
):
    return crud.follow.get_all_follows(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.Follow)
def get_follow_by_id(
    id: int,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
):
    db_follow = crud.follow.get_follow_by_id(db, id=id)

    if db_follow is None:
        raise HTTPException(status_code=404, detail="Follow not found")

    return db_follow


@router.post("/{following_id}", response_model=schemas.Follow)
def follow_user(
    following_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_user = crud.user.get_active_user_by_id(db, id=following_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if following_id == current_user.id:
        raise HTTPException(
            status_code=400, detail="You can't follow yourself"
        )

    db_follow = crud.follow.get_follow_by_follower_id_and_following_id(
        db, follower_id=current_user.id, following_id=following_id
    )

    if db_follow:
        raise HTTPException(
            status_code=400, detail="You already followed this user"
        )

    return crud.follow.follow(db, follower_id=current_user.id, following_id=following_id)


@router.delete("/{following_id}", response_model=schemas.Follow)
def unfollow_user(
    following_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_user = crud.user.get_active_user_by_id(db, id=following_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if following_id == current_user.id:
        raise HTTPException(
            status_code=400, detail="You can't unfollow yourself"
        )

    db_follow = crud.follow.get_follow_by_follower_id_and_following_id(
        db, follower_id=current_user.id, following_id=following_id
    )

    if db_follow is None:
        raise HTTPException(
            status_code=400, detail="You have not followed this user"
        )

    return crud.follow.unfollow(db, follower_id=current_user.id, following_id=following_id)


@router.get("/count/", response_model=int)
def get_all_follows_count(
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db)
):
    return crud.follow.get_all_follows_count(db)


@router.get("/follower/count/{user_id}", response_model=int)
def get_follower_count_by_user_id(
    user_id: int,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db)
):
    db_user = crud.user.get_user_by_id(db, id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.follow.get_followers_count_by_user_id(db, user_id=user_id)


@router.get("/follower/ids/{user_id}", response_model=list[schemas.Id])
def get_follower_ids_by_user_id(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
):
    db_user = crud.user.get_user_by_id(db, id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.follow.get_followers_by_user_id(db, user_id=user_id, skip=skip, limit=limit)


@router.get("/following/count/{user_id}", response_model=int)
def get_following_count_by_user_id(
    user_id: int,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db)
):
    db_user = crud.user.get_user_by_id(db, id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.follow.get_followings_count_by_user_id(db, user_id=user_id)


@router.get("/following/ids/{user_id}", response_model=list[schemas.Id])
def get_following_ids_by_user_id(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
):
    db_user = crud.user.get_user_by_id(db, id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.follow.get_followings_by_user_id(db, user_id=user_id, skip=skip, limit=limit)
