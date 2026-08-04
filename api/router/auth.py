from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. models import User
from ..db.database import engine, get_db
from ..schemas import schemas
from ..services import oauth2
from ..utls import utils

router = APIRouter(
    tags= ["Auth"]
)



@router.post('/login', response_model = schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code =status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')
    if not utils.verify(user_credentials.password, user.password): 
        raise HTTPException(status_code =status.HTTP_403_FORBIDDEN, detail=f'Inva lid credentials')


    access_token = oauth2.create_access_token(data = {"user_id": user.id })

    return {"access_token": access_token, "token_type": "bearer"}