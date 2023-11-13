from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import database, models
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
  to_encode = data.copy()
  expire_time = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
  to_encode.update({"exp": expire_time})

  encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

  return encoded_jwt

def verify_access_token(token: schemas.Token, credentials_exception):
  
  try:
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id")

    if id is None:
      raise credentials_exception

    token_data = schemas.TokenData(id=id)
  except JWTError:
    raise credentials_exception

  return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Invalid Credentials",
    headers={"WWW-Authenticate": "Bearer"}
  )

  token = verify_access_token(token, credentials_exception)
  user = db.query(models.User).filter(models.User.id == token.id).first()

  return user
