'''User Routes'''
import typing as ty

from fastapi import Depends, HTTPException, Response, status, APIRouter
import sqlalchemy
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import oauth2

from .. import models, schemas
from ..database import get_db


router = APIRouter(
  prefix="/posts",
  tags=['Posts']
)

# @router.get("/")
@router.get("/", response_model=ty.List[schemas.PostOut])
def get_posts(
  db: Session = Depends(get_db), 
  limit: int = 10,
  skip: int = 0,
  search: ty.Optional[str] = ""

  ):
  # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

  results = (db
    .query(models.Post, sqlalchemy.func.count(models.Vote.post_id).label("num_votes"))
    .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
    .group_by(models.Post.id)
    .filter(models.Post.title.contains(search))
    .order_by(sqlalchemy.desc('created_at'))
    .limit(limit)
    .offset(skip)
    .all()
    )
  return results


@router.get("/latest")
def get_latest_post(db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):

  post = db.query(models.Post).order_by(desc(models.Post.created_at)).limit(1).first()

  return post

@router.get("/{id}", response_model=schemas.Post)
def get_post(
  id: int, db: Session = Depends(get_db), 
):

  post = db.query(models.Post).where(models.Post.id == id).first()

  if not post:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail=f"Post with id: {id} was not found"
    )
    
  return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
  post: schemas.PostCreate, 
  db: Session = Depends(get_db), 
  user: models.User = Depends(oauth2.get_current_user)
):

  new_post = models.Post(**post.dict(), user_id=user.id)
  db.add(new_post)
  db.commit()
  db.refresh(new_post)

  return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):

  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()


  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
  elif post.user_id != user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with id: {user.id} does not own the post with id: {id}")
  else:
    post_query.delete(synchronize_session=False)
    db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
  id: int, 
  post: schemas.PostCreate, 
  db: Session = Depends(get_db), 
  user: models.User = Depends(oauth2.get_current_user)
):

  post_query = db.query(models.Post).filter(models.Post.id == id)
  post_db = post_query.first()

  if not post_db:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
  elif post_db.user_id != user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with id: {user.id} does not own the post with id: {id}")
  else:
    post_upd = {**post.dict(), **{'user_id': user.id}}
    post_query.update(post_upd, synchronize_session=False)
    db.commit()

  return post_query.first()
