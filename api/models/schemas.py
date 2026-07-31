from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from  typing import Optional
from pydantic.types import conint

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    createdDate: datetime

class UserForgotPassword:
    token: str

class UserLogin(BaseModel):
    email:EmailStr
    password: str


class PostBase(BaseModel):
    title :str
    content : str
    published : bool = True 


class PostCreate(PostBase):
    pass



class Post(PostBase):
    id: int
    userId: int
    owner: UserOut
    createdDate: datetime
    class Config:
        from_attributes = True


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    userId: int
    createdDate: datetime
    owner: UserOut
    votes: int

    class Config:
        from_attributes = True



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id : Optional[int] = None


class Vote(BaseModel):
    postId: int
    dir: conint(le=1)