from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.get("/all", response_model=list[schemas.Follow])
def get_all_follows(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):
    return crud.follow.get_all(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.Follow)
def get_follow_by_id(
    id: int,
    db: Session = Depends(deps.get_db),
):
    db_follow = crud.follow.get_by_id(db, id=id)

    if db_follow is None:
        raise HTTPException(status_code=404, detail="Follow not found")

    return db_follow


@router.get("/follower/count/{follower_id}", response_model=int)
def get_follows_count_follower_id(
    follower_id: int,
    db: Session = Depends(deps.get_db)
):
    db_user = crud.user.get_by_id(db, id=follower_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.follow.get_count_by_follower_id(db, follower_id=follower_id)


@router.get("/follower/ids/{follower_id}", response_model=list[schemas.Id])
def get_follows_ids_by_follower_id(
    follower_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
):
    db_user = crud.user.get_by_id(db, id=follower_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.follow.get_by_follower_id(db, follower_id=follower_id, skip=skip, limit=limit)


@router.get("/following/count/{following_id}", response_model=int)
def get_follows_count_following_id(
    following_id: int,
    db: Session = Depends(deps.get_db)
):
    db_user = crud.user.get_by_id(db, id=following_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.follow.get_count_by_following_id(db, following_id=following_id)


@router.get("/following/ids/{following_id}", response_model=list[schemas.Id])
def get_follows_ids_by_following_id(
    following_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
):
    db_user = crud.user.get_by_id(db, id=following_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.follow.get_by_following_id(db, following_id=following_id, skip=skip, limit=limit)


@router.post("/{following_id}", response_model=schemas.Follow)
def follow_user(
    following_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_user = crud.user.get_by_id(db, id=following_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if following_id == current_user.id:
        raise HTTPException(
            status_code=400, detail="You can't follow yourself"
        )

    db_follow = crud.follow.get_follow(
        db, follower_id=current_user.id, following_id=following_id
    )

    if db_follow is not None:
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
    db_user = crud.user.get_by_id(db, id=following_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if following_id == current_user.id:
        raise HTTPException(
            status_code=400, detail="You can't unfollow yourself"
        )
    db_follow = crud.follow.get_follow(
        db, follower_id=current_user.id, following_id=following_id
    )

    if db_follow is None:
        raise HTTPException(
            status_code=400, detail="You have not followed this user"
        )

    return crud.follow.unfollow(db, follower_id=current_user.id, following_id=following_id)
