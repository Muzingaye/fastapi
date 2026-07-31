
from .. models import models, schemas, utils
from .. models.database import engine, get_db
from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags= ["Users"]

)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model =schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    print("hashed_password: ", user.password)

    print("Len, :" , len(user.password.encode("utf-8")))
    new_user = models.User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model =schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail=f'user with id: {id} was not found')
    return user
