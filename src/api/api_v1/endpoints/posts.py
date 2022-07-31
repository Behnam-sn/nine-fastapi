from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.Post])
def get_all_posts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):
    db_posts = crud.post.get_all_posts(db, skip=skip, limit=limit)
    return [crud.post.render_post_with_author(db, post=db_post) for db_post in db_posts]


@router.get("/{id}", response_model=schemas.Post)
def get_post_by_id(
    id: int,
    db: Session = Depends(deps.get_db),
):
    db_post = crud.post.get_post_by_id(db, id=id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return crud.post.render_post_with_author(db, post=db_post)


@router.post("/", response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_post = crud.post.create_post(db, post=post, author_id=current_user.id)
    return crud.post.render_post_with_author(db, post=db_post)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    post_update: schemas.PostUpdate,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_post = crud.post.get_post_by_id(db, id=id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=400, detail="Permission denied")

    db_updated_post = crud.post.update_post(db, id=id, post_update=post_update)
    return crud.post.render_post_with_author(db, post=db_updated_post)
