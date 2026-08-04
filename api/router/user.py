
from .. models import User
from ..db.database import engine, get_db
from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..schemas import schemas
from ..utls import utils

router = APIRouter(
    prefix="/user",
    tags= ["Users"]

)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model =schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()
    print("user", db_user)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model =schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail=f'user with id: {id} was not found')
    return user



# @router.get("/{email}", response_class=schemas.UserForgotPassword)
# def forgot_password(email: str, db: Session = Depends(get_db)):
#     res = db.execute(
#         select(models.User).where(
#             func.lower(models.User.email) == email # replacen this requesteddata
#         )
#     )

#     user = res.scalar().first()