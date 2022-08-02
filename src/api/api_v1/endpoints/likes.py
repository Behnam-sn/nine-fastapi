from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.Like])
def get_all_likes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):
    return crud.like.get_all(db, skip=skip, limit=limit)


@router.post("/post/{post_id}", response_model=schemas.PostLike)
def like_post(
    post_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_post = crud.post.get_by_id(db, id=post_id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    db_like = crud.like.get_post_like(
        db, post_id=post_id, owner_id=current_user.id
    )

    if db_like is not None:
        raise HTTPException(
            status_code=400, detail="You already liked this post"
        )

    return crud.like.like_post(db, post_id=post_id, owner_id=current_user.id)


@router.delete("/post/{post_id}", response_model=schemas.PostLike)
def unlike_post(
    post_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_post = crud.post.get_by_id(db, id=post_id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    db_like = crud.like.get_post_like(
        db, post_id=post_id, owner_id=current_user.id
    )

    if db_like is None:
        raise HTTPException(
            status_code=400, detail="You have not liked this post"
        )

    return crud.like.unlike_post(db, post_id=post_id, owner_id=current_user.id)


@router.post("/comment/{comment_id}", response_model=schemas.CommentLike)
def like_comment(
    comment_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_comment = crud.comment.get_by_id(db, id=comment_id)

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    db_like = crud.like.get_comment_like(
        db, comment_id=comment_id, owner_id=current_user.id
    )

    if db_like is not None:
        raise HTTPException(
            status_code=400, detail="You already liked this comment"
        )

    return crud.like.like_comment(db, comment_id=comment_id, owner_id=current_user.id)


@router.delete("/comment/{comment_id}", response_model=schemas.CommentLike)
def unlike_comment(
    comment_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_comment = crud.comment.get_by_id(db, id=comment_id)

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    db_like = crud.like.get_comment_like(
        db, comment_id=comment_id, owner_id=current_user.id
    )

    if db_like is None:
        raise HTTPException(
            status_code=400, detail="You have not liked this comment"
        )

    return crud.like.unlike_comment(db, comment_id=comment_id, owner_id=current_user.id)
