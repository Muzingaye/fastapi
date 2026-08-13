from sqlalchemy.orm import Session

from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)

from ..db.database import engine, get_db
from ..models import Vote
from ..schemas import schemas
from ..services.utls import oauth2
from ..utls import utils

router = APIRouter(
    prefix="/vote",
    tags= ["Votes"]

)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post =  vote_qy = db.query(Vote).filter(Vote.postId == vote.postId)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post does not exists')

    vote_qy = db.query(Vote).filter(Vote.postId == vote.postId, Vote.userId == current_user.id)
    found = vote_qy.first()
    if(vote.dir == 1):
        if found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'use { current_user.id} has already voted on post {vote.postId}')
        new_vote = Vote(userId = current_user.id, postId = vote.postId )
        db.add(new_vote)
        db.commit()
        return {"message": "Success added vote"}
    else:
        if not found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Vote does not exists')
        vote_qy.delete(synchronize_session=False)
        db.commit()
        return {"message": "Success deleted vote"}
