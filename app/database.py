from sqlalchemy.engine import URL as SQLAlchemyURL, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


sqlalchemy_database_url_obj = SQLAlchemyURL(
  "postgresql",
  username=settings.database_username,
  password=settings.database_password,
  host=settings.database_hostname,
  database=settings.database_name,
  port=settings.database_port
)
engine = create_engine(sqlalchemy_database_url_obj)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependancy
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()