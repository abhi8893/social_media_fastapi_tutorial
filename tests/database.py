from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from app.config import settings
from sqlalchemy.engine import create_engine, URL as SQLAlchemyURL
from sqlalchemy.orm import sessionmaker
import pytest


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

@pytest.fixture(scope='function')
def session():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()


@pytest.fixture(scope='function')
def client(session):
  def override_get_db():
    try:
      yield session
    finally:
      session.close()

  app.dependency_overrides[get_db] = override_get_db

  yield TestClient(app)