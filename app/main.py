from fastapi import FastAPI, status, Response, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import pyodbc
import time
from .models import models
from .models.database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)


while True:
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=FastApi;"
            "DATABASE=FastApi;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        cursor = conn.cursor()
        print('Database was successful')
        break
    except Exception as err:
        print("Connection to database failed.")
        print("Error ", err)
        time.sleep(5)




@app.get('/posts')
def get_post(db: Session = Depends(get_db)):
    posts  = db.query(models.Post).all()
    return {"data": posts}


@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
    return {"data": post}


@app.post( '/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: dict, db: Session = Depends(get_db)):
    new_post = models.Post(**post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.delete('/posts/{id}')
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
            raise HTTPException(status_code =status.HTTP_204_NO_CONTENT, detail=f'post with id: {id} was not found')
    # post.delete(synchronize_session=False)
    db.delete(post)
    db.commit()
    return



@app.put('/posts/{id}')
def update_post(id: int, post: dict, db: Session = Depends(get_db)):

    db_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not db_post:
            raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
    
    for k, v in post.items():
         setattr(db_post, k, v)
    
    db.commit()
    db.refresh(db_post)
    return {"data": db_post}
