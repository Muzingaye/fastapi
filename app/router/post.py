
from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. models import models, schemas, oauth2
from .. models.database import engine, get_db


router = APIRouter(
    prefix="/posts",
    tags= ["Posts"]
)

# @router.get('/',  response_model=List[schemas.Post])
@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip=0, search: Optional[str] = "" ):
    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(search))
    #     .order_by(models.Post.createdDate.desc()).limit(limit).offset(skip)
    #     .all()
    # )

    results = (db.query(models.Post, 
                        func.count(models.Vote.postId).label("votes")
                        )
               .outerjoin(models.Vote, 
                          models.Vote.postId== models.Post.id)
               .group_by(
                    models.Post.id,
                    models.Post.title,
                    models.Post.content,
                    models.Post.published,
                    models.Post.createdDate,
                    models.Post.userId
                    )
                    .order_by(models.Post.createdDate.desc())
                    .limit(limit)
                    .offset(skip)
                    .all())
    
    return [
         {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "published": post.published,
            "userId": post.userId,
            "createdDate": post.createdDate,
            "owner": post.owner,
            "votes": votes
         }
         for post, votes in results
    ]

@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
    return post


@router.post( '/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.model_dump(), userId=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
            raise HTTPException(status_code =status.HTTP_204_NO_CONTENT, detail=f'post with id: {id} was not found')

    if post.userId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )
        
    # post.delete(synchronize_session=False)
    db.delete(post)
    db.commit()
    return



@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    db_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not db_post:
            raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')

    if db_post.userId != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this post"
            )
    
    for k, v in post.model_dump().items():
         setattr(db_post, k, v)
    
    db.commit()
    db.refresh(db_post)
    return db_post
