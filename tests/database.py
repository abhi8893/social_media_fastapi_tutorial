from app.config import settings
from sqlalchemy.engine import create_engine, URL as SQLAlchemyURL
from sqlalchemy.orm import sessionmaker


sqlalchemy_database_url_obj = SQLAlchemyURL.create(
  "postgresql",
  username=settings.database_username,
  password=settings.database_password,
  host=settings.database_hostname,
  database=f'{settings.database_name}_test',
  port=settings.database_port
)
engine = create_engine(sqlalchemy_database_url_obj)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

