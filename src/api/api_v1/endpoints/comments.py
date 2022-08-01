from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Comment)
def create_comment(
    comment: schemas.CommentCreate,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    return crud.comment.create(db, comment=comment, owner_id=current_user.id)


@router.get("/", response_model=list[schemas.Comment])
def get_all_comments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):
    return crud.comment.get_all(db, skip=skip, limit=limit)


@router.put("/{id}", response_model=schemas.Comment)
def update_comment(
    id: int,
    comment_update: schemas.CommentUpdate,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_comment = crud.comment.get_by_id(db, id=id)

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    if db_comment.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Permission Denied")

    return crud.comment.update(db, id=id, comment_update=comment_update)


@router.put("/activate/{id}", response_model=schemas.Comment)
def activate_comment(
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    db_comment = crud.comment.get_by_id(db, id=id)

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    if current_user.is_superuser is False and current_user.id != db_comment.owner_id:
        raise HTTPException(status_code=400, detail="Not Authenticated")

    return crud.comment.active(db, id=id)


@router.put("/deactivate/{id}", response_model=schemas.Comment)
def deactivate_comment(
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    db_comment = crud.comment.get_by_id(db, id=id)

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    if current_user.is_superuser is False and current_user.id != db_comment.owner_id:
        raise HTTPException(status_code=400, detail="Not Authenticated")

    return crud.comment.deactive(db, id=id)


@router.delete("/{id}", response_model=schemas.Comment)
def delete_comment(
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_comment = crud.comment.get_by_id(db, id=id)

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Permission Denied")

    return crud.comment.delete(db, id=id)
