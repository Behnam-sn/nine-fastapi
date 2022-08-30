from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud, schemas
from src.api import deps

router = APIRouter()


@router.get("/all/", response_model=list[schemas.Comment])
def get_all_active_comments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):
    return crud.comment.get_all_active_comments(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.Comment)
def get_active_comment_by_id(
    id: int,
    db: Session = Depends(deps.get_db),
):
    db_comment = crud.comment.get_active_comment_by_id(db, id=id)

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    return db_comment


@router.get("/count/", response_model=int)
def get_all_active_comments_count(
    db: Session = Depends(deps.get_db)
):
    return crud.comment.get_all_active_comments_count(db)


@router.get("/ids/", response_model=list[schemas.Id])
def get_all_active_comments_ids(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):
    return crud.comment.get_all_active_comments(db, skip=skip, limit=limit)


@router.get("/owner/count/{owner_id}", response_model=int)
def get_active_comments_count_by_owner_id(
    owner_id: int,
    db: Session = Depends(deps.get_db)
):
    db_user = crud.user.get_active_user_by_id(db, id=owner_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.comment.get_active_comments_count_by_owner_id(db, owner_id=owner_id)


@router.get("/owner/ids/{owner_id}", response_model=list[schemas.Id])
def get_active_comments_ids_by_owner_id(
    owner_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
):
    db_user = crud.user.get_active_user_by_id(db, id=owner_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.comment.get_active_comments_by_owner_id(db, owner_id=owner_id, skip=skip, limit=limit)


@router.get("/post/count/{post_id}", response_model=int)
def get_active_comments_count_by_post_id(
    post_id: int,
    db: Session = Depends(deps.get_db)
):
    db_post = crud.post.get_active_post_by_id(db, id=post_id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return crud.comment.get_active_comments_count_by_post_id(db, post_id=post_id)


@router.get("/post/ids/{post_id}", response_model=list[schemas.Id])
def get_active_comments_ids_by_post_id(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
):
    db_post = crud.post.get_active_post_by_id(db, id=post_id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return crud.comment.get_active_comments_by_post_id(db, post_id=post_id, skip=skip, limit=limit)
