import logging
from .log_conf import log_config
from . import models
from .database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, vote


# This creates all the tables from the models
models.Base.metadata.create_all(bind=engine)

# setup loggers
logging.config.dictConfig(log_config)

# get root logger
logger = logging.getLogger(__name__)

# app
app = FastAPI(debug=True)

# origins = ['https://www.google.com']
origins = []

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def root():
  return {'message': 'Welcome to my improved app!'}








  
  

