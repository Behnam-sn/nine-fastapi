from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.get("/all/", response_model=list[schemas.Like])
def get_all_likes(
    skip: int = 0,
    limit: int = 100,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db)
):
    return crud.like.get_all_likes(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.Like)
def get_like_by_id(
    id: int,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
):
    db_like = crud.like.get_like_by_id(db, id=id)

    if db_like is None:
        raise HTTPException(status_code=404, detail="Like not found")

    return db_like


@router.get("/is-post-liked/{post_id}", response_model=bool)
def get_is_post_liked(
    post_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_like = crud.like.get_like_by_post_id_and_owner_id(
        db, owner_id=current_user.id, post_id=post_id
    )

    return db_like is not None


@router.get("/is-comment-liked/{comment_id}", response_model=bool)
def get_is_comment_liked(
    comment_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_like = crud.like.get_like_by_comment_id_and_owner_id(
        db, owner_id=current_user.id, comment_id=comment_id
    )

    return db_like is not None


@router.post("/post/{post_id}", response_model=schemas.Like)
def like_post(
    post_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_post = crud.post.get_active_post_by_id(db, id=post_id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    db_like = crud.like.get_like_by_post_id_and_owner_id(
        db, post_id=post_id, owner_id=current_user.id
    )

    if db_like:
        raise HTTPException(
            status_code=400, detail="You already liked this post"
        )

    return crud.like.like_post(db, post_id=post_id, owner_id=current_user.id)


@router.delete("/post/{post_id}", response_model=schemas.Like)
def unlike_post(
    post_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_post = crud.post.get_active_post_by_id(db, id=post_id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    db_like = crud.like.get_like_by_post_id_and_owner_id(
        db, post_id=post_id, owner_id=current_user.id
    )

    if db_like is None:
        raise HTTPException(
            status_code=400, detail="You have not liked this post"
        )

    return crud.like.unlike_post(db, post_id=post_id, owner_id=current_user.id)


@router.post("/comment/{comment_id}", response_model=schemas.Like)
def like_comment(
    comment_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_comment = crud.comment.get_active_comment_by_id(db, id=comment_id)

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    db_like = crud.like.get_like_by_comment_id_and_owner_id(
        db, comment_id=comment_id, owner_id=current_user.id
    )

    if db_like:
        raise HTTPException(
            status_code=400, detail="You already liked this comment"
        )

    return crud.like.like_comment(db, comment_id=comment_id, owner_id=current_user.id)


@router.delete("/comment/{comment_id}", response_model=schemas.Like)
def unlike_comment(
    comment_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_comment = crud.comment.get_active_comment_by_id(db, id=comment_id)

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    db_like = crud.like.get_like_by_comment_id_and_owner_id(
        db, comment_id=comment_id, owner_id=current_user.id
    )

    if db_like is None:
        raise HTTPException(
            status_code=400, detail="You have not liked this comment"
        )

    return crud.like.unlike_comment(db, comment_id=comment_id, owner_id=current_user.id)


@router.get("/count/", response_model=int)
def get_all_likes_count(
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db)
):
    return crud.like.get_all_likes_count(db)


@router.get("/owner/count/{owner_id}", response_model=int)
def get_likes_count_by_owner_id(
    owner_id: int,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db)
):
    db_user = crud.user.get_user_by_id(db, id=owner_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.like.get_likes_count_by_owner_id(db, owner_id=owner_id)


@router.get("/owner/ids/{owner_id}", response_model=list[schemas.Id])
def get_likes_ids_by_owner_id(
    owner_id: int,
    skip: int = 0,
    limit: int = 100,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
):
    db_user = crud.user.get_user_by_id(db, id=owner_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.like.get_likes_by_owner_id(db, owner_id=owner_id, skip=skip, limit=limit)


@router.get("/post/count/{post_id}", response_model=int)
def get_likes_count_by_post_id(
    post_id: int,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db)
):
    db_post = crud.post.get_post_by_id(db, id=post_id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return crud.like.get_likes_count_by_post_id(db, post_id=post_id)


@router.get("/post/ids/{post_id}", response_model=list[schemas.Id])
def get_likes_ids_by_post_id(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
):
    db_post = crud.post.get_post_by_id(db, id=post_id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return crud.like.get_likes_by_post_id(db, post_id=post_id, skip=skip, limit=limit)


@router.get("/comment/count/{comment_id}", response_model=int)
def get_likes_count_by_comment_id(
    comment_id: int,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db)
):
    db_comment = crud.comment.get_comment_by_id(db, id=comment_id)

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    return crud.like.get_likes_count_by_comment_id(db, comment_id=comment_id)


@router.get("/comment/ids/{comment_id}", response_model=list[schemas.Id])
def get_likes_ids_by_comment_id(
    comment_id: int,
    skip: int = 0,
    limit: int = 100,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
):
    db_comment = crud.comment.get_comment_by_id(db, id=comment_id)

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    return crud.like.get_likes_by_comment_id(db, comment_id=comment_id, skip=skip, limit=limit)
