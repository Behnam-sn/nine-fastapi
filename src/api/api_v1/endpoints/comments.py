from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.get("/all/", response_model=list[schemas.Comment])
def get_all_comments(
    skip: int = 0,
    limit: int = 100,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db)
):
    return crud.comment.get_all_comments(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Comment)
def create_comment(
    comment: schemas.CommentCreate,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_post = crud.post.get_active_post_by_id(db, id=comment.post_id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return crud.comment.create(db, comment=comment, owner_id=current_user.id)


@router.get("/{id}", response_model=schemas.Comment)
def get_comment_by_id(
    id: int,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
):
    db_comment = crud.comment.get_comment_by_id(db, id=id)

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    return db_comment


@router.put("/{id}", response_model=schemas.Comment)
def update_comment(
    id: int,
    comment_update: schemas.CommentUpdate,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_comment = crud.comment.get_active_comment_by_id(db, id=id)

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    if db_comment.owner_id != current_user.id:
        raise HTTPException(status_code=401, detail="Permission Denied")

    return crud.comment.update(db, id=id, comment_update=comment_update)


@router.delete("/{id}")
def delete_comment(
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_comment = crud.comment.get_comment_by_id(db, id=id)

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Permission Denied")

    crud.comment.delete(db, id=id)


@router.put("/activate/{id}", response_model=schemas.Comment)
def activate_comment(
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    db_comment = crud.comment.get_comment_by_id(db, id=id)

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Not Authenticated")

    return crud.comment.activate(db, id=id)


@router.put("/deactivate/{id}", response_model=schemas.Comment)
def deactivate_comment(
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    db_comment = crud.comment.get_active_comment_by_id(db, id=id)

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    if current_user.is_superuser is False and current_user.id != db_comment.owner_id:
        raise HTTPException(status_code=401, detail="Not Authenticated")

    return crud.comment.deactivate(db, id=id)


@router.get("/count/", response_model=int)
def get_all_comments_count(
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db)
):
    return crud.comment.get_all_comments_count(db)


@router.get("/ids/", response_model=list[schemas.Id])
def get_all_comments_ids(
    skip: int = 0,
    limit: int = 100,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db)
):
    return crud.comment.get_all_comments(db, skip=skip, limit=limit)


@router.get("/owner/count/{owner_id}", response_model=int)
def get_comments_count_by_owner_id(
    owner_id: int,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db)
):
    db_user = crud.user.get_user_by_id(db, id=owner_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.comment.get_comments_count_by_owner_id(db, owner_id=owner_id)


@router.get("/owner/ids/{owner_id}", response_model=list[schemas.Id])
def get_comments_ids_by_owner_id(
    owner_id: int,
    skip: int = 0,
    limit: int = 100,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
):
    db_user = crud.user.get_user_by_id(db, id=owner_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.comment.get_comments_by_owner_id(db, owner_id=owner_id, skip=skip, limit=limit)


@router.get("/post/count/{post_id}", response_model=int)
def get_comments_count_by_post_id(
    post_id: int,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db)
):
    db_post = crud.post.get_post_by_id(db, id=post_id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return crud.comment.get_comments_count_by_post_id(db, post_id=post_id)


@router.get("/post/ids/{post_id}", response_model=list[schemas.Id])
def get_comments_ids_by_post_id(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    super_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
):
    db_post = crud.post.get_post_by_id(db, id=post_id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return crud.comment.get_comments_by_post_id(db, post_id=post_id, skip=skip, limit=limit)
