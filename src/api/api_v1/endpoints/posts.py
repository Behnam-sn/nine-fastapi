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


@router.post("/", response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    return crud.post.create(db, post=post, owner_id=current_user.id)


@router.get("/{id}", response_model=schemas.Post)
def get_active_post_by_id(
    id: int,
    db: Session = Depends(deps.get_db),
):
    db_post = crud.post.get_by_id(db, id=id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if not db_post.is_active:
        raise HTTPException(status_code=403, detail="Post is not available")

    return db_post


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    post_update: schemas.PostUpdate,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_post = crud.post.get_by_id(db, id=id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if not db_post.is_active:
        raise HTTPException(status_code=403, detail="Post is not available")

    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=401, detail="Permission Denied")

    return crud.post.update(db, id=id, post_update=post_update)


@router.delete("/{id}")
def delete_post(
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_post = crud.post.get_by_id(db, id=id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Permission Denied")

    crud.post.delete(db, id=id)


@router.put("/activate/{id}", response_model=schemas.Post)
def activate_post(
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    db_post = crud.post.get_by_id(db, id=id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Not Authenticated")

    return crud.post.active(db, id=id)


@router.put("/deactivate/{id}", response_model=schemas.Post)
def deactivate_post(
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    db_post = crud.post.get_by_id(db, id=id)

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if current_user.is_superuser is False and current_user.id != db_post.owner_id:
        raise HTTPException(status_code=401, detail="Not Authenticated")

    return crud.post.deactive(db, id=id)


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
    db_user = crud.user.get_by_id(db, id=owner_id)

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
    db_user = crud.user.get_by_id(db, id=owner_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.post.get_active_posts_by_owner_id(db, owner_id=owner_id, skip=skip, limit=limit)
