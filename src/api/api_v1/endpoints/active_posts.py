from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.get("/all/", response_model=list[schemas.Post])
def get_all_active_posts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):
    return crud.post.get_all_active_posts(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.Post)
def get_active_post_by_id(
    id: int,
    db: Session = Depends(deps.get_db),
):
    db_post = crud.post.get_active_post_by_id(db, id=id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return db_post


@router.get("/count/", response_model=int)
def get_all_active_posts_count(
    db: Session = Depends(deps.get_db)
):
    return crud.post.get_all_active_posts_count(db)


@router.get("/ids/", response_model=list[schemas.Id])
def get_all_active_posts_ids(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):
    return crud.post.get_all_active_posts(db, skip=skip, limit=limit)


@router.get("/owner/count/{owner_id}", response_model=int)
def get_active_posts_count_by_owner_id(
    owner_id: int,
    db: Session = Depends(deps.get_db)
):
    db_user = crud.user.get_active_user_by_id(db, id=owner_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.post.get_active_posts_count_by_owner_id(db, owner_id=owner_id)


@router.get("/owner/ids/{owner_id}", response_model=list[schemas.Id])
def get_active_posts_ids_by_owner_id(
    owner_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
):
    db_user = crud.user.get_active_user_by_id(db, id=owner_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.post.get_active_posts_by_owner_id(db, owner_id=owner_id, skip=skip, limit=limit)
