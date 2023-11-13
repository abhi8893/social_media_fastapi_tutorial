from os import access
from jose import jwt, JWTError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, models, schemas, utils, oauth2


router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: database.SessionLocal = Depends(database.get_db)):
  user = db.query(models.User).where(models.User.email == user_creds.username).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
  
  if not utils.verify_password(user_creds.password, user.password):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

  # Create JWT Token
  access_token = oauth2.create_access_token(data = {"user_id": user.id})

  return {'access_token': access_token, "token_type": "bearer"}
      



  
