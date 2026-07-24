
from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. models import models, schemas, oauth2
from .. models.database import engine, get_db


router = APIRouter(
    prefix="/posts",
    tags= ["Posts"]
)

@router.get('/',  response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    posts  = db.query(models.Post).all()
    return posts

@router.get('//{id}', response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
    return post


@router.post( '/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
            raise HTTPException(status_code =status.HTTP_204_NO_CONTENT, detail=f'post with id: {id} was not found')
    # post.delete(synchronize_session=False)
    db.delete(post)
    db.commit()
    return



@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):

    db_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not db_post:
            raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
    
    for k, v in post.model_dump().items():
         setattr(db_post, k, v)
    
    db.commit()
    db.refresh(db_post)
    return db_post
