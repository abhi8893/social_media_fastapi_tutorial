""""""
import pytest
from app.database import get_db, Base
from .database import app, engine, TestingSessionLocal
from fastapi.testclient import TestClient


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

@pytest.fixture()
def test_user(client):
  user_info = {'email': 'user1@gmail.com', 'password': 'user@1'}
  res = client.post('/users/', json=user_info)
  new_user = res.json()
  new_user['password'] = user_info['password']

  return new_user