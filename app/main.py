from fastapi import FastAPI, status, Response, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import pyodbc
import time
from .models import models, schemas, utils
from .models.database import engine, get_db
from sqlalchemy.orm import Session
from typing import Optional, List

from .router import user, post


models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

app.include_router(user.router)
app.include_router(post.router)


