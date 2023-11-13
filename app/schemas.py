from datetime import datetime
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
import typing as ty

from app.database import Base

class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True


class PostCreate(PostBase):
  pass

class UserOut(BaseModel):
  id: int
  email: EmailStr
  created_at: datetime

  class Config:
    orm_mode = True

class Post(PostBase):
  id: int
  user_id: int
  user: UserOut
  created_at: datetime

  class Config:
    orm_mode = True


class PostOut(BaseModel):
  Post: Post
  num_votes: int

  class Config:
    orm_mode = True


class UserCreate(BaseModel):
  email: EmailStr
  password: str

class UserLogin(BaseModel):
  email: EmailStr
  password: str

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: ty.Optional[int]


class Vote(BaseModel):
  post_id: int
  direction: conint(le=1)
