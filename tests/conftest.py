""""""
import pytest
from app.main import app
from app.database import get_db, Base
from .database import engine, TestingSessionLocal
from fastapi.testclient import TestClient
from app import oauth2, models


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


@pytest.fixture()
def test_user2(client):
  user_info = {'email': 'user2@gmail.com', 'password': 'user@2'}
  res = client.post('/users/', json=user_info)
  new_user = res.json()
  new_user['password'] = user_info['password']

  return new_user


## NOTE: Below is for user1 aka test_user only!
@pytest.fixture
def token(test_user):
  return oauth2.create_access_token(data = {"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
  client.headers = {
    **client.headers,
    'Authorization': f'Bearer {token}'
  }
  return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
  posts_list = [
    {'title': '1st post', 'content': '1st content', 'user_id': test_user['id']},
    {'title': '2nd post', 'content': '2nd content', 'user_id': test_user['id']},
    {'title': '3rd post', 'content': '3rd content', 'user_id': test_user['id']},
    {'title': '4th post', 'content': '4th content', 'user_id': test_user2['id']},
  ]

  posts_obj = [models.Post(**d) for d in posts_list]

  session.add_all(posts_obj)
  session.commit()
  posts = session.query(models.Post).all()
  
  return posts