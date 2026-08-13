
import uuid
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from fastapi import (APIRouter, Cookie, Depends, FastAPI, HTTPException,
                     Response, status)

from ..db.database import engine, get_db
from ..models import Post, User, Vote
from ..schemas import job, schemas
from ..services.utls import oauth2

router = APIRouter(
    prefix="/posts",
    tags= ["Posts"]
)

def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
        print(session_id)
    return session_id

@router.post('/create', response_model=job.StoryJobCreate)
def create_session(request: job.StoryJobCreate, background_tasks: dict, 
                   response: Response, session_id: str= Depends(get_session_id)):
     pass
# @router.get('/',  response_model=List[schemas.Post])
@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip=0, search: Optional[str] = "" ):
    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(search))
    #     .order_by(models.Post.createdDate.desc()).limit(limit).offset(skip)
    #     .all()
    # )

    results = (db.query(Post, 
                        func.count(Vote.postId).label("votes")
                        )
               .outerjoin(Vote, 
                          Vote.postId== Post.id)
                .filter(Post.title.contains(search))
               .group_by(
                    Post.id,
                    Post.title,
                    Post.content,
                    Post.published,
                    Post.createdDate,
                    Post.userId
                    )
                    .order_by(Post.createdDate.desc())
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

@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    # post = (db.query(models.Post, func.count(models.Vote.postId).label("Votes"))
    #     .join(models.Vote, models.Vote.postId == models.Post.id, isouter=True)
    #     .group_by(models.Post.id)
    #     .filter(models.Post.id == id).first()
    #     )
    
    results = (db.query(Post, 
                            func.count(Vote.postId).label("votes")
                            )
                   .outerjoin(Vote, 
                              Vote.postId== Post.id)
                    .where(Post.id == id)
                   .group_by(
                        Post.id,
                        Post.title,
                        Post.content,
                        Post.published,
                        Post.createdDate,
                        Post.userId
                        )
                        .order_by(Post.createdDate.desc())
                        .first())

    if not results:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')


    post, votes = results
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "published": post.published,
        "userId": post.userId,
        "createdDate": post.createdDate,
        "owner": post.owner,
        "votes": votes
    }
    
    # return results


@router.post( '/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    new_post = Post(**post.model_dump(), userId=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



# async def upload_file(file: UploadFIle = File(...), caption: str = Form(""), db: Session = Depends(get_db)):
#      pass


@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    post = db.query(Post).filter(Post.id == id).first()
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

    db_post = db.query(Post).filter(Post.id == id).first()
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
