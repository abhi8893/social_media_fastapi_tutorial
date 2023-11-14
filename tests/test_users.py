"""Tests for users route"""
from app import schemas, models
import pytest
from jose import jwt
from app.config import settings


def test_root(client):
  res = client.get('/')
  assert res.json()['message'] == 'Welcome to my app!'
  assert res.status_code == 200

def test_create_user(client):
  res = client.post('/users/', json={'email': 'user1@gmail.com', 'password': 'user@1'})
  user = schemas.UserOut(**res.json())
  assert res.status_code == 201
  assert user.email == 'user1@gmail.com'


def test_login_user(client, test_user):
  res = client.post('/login', data={'username': test_user['email'], 'password': test_user['password']})
  token = schemas.Token(**res.json())
  payload = jwt.decode(token.access_token, settings.secret_key, algorithms=[settings.algorithm])

  assert res.status_code == 200
  assert test_user['id'] == payload['user_id']
  assert token.token_type == 'bearer'


@pytest.mark.parametrize(
  "email, password, status_code",[
    ('wrongemail@gmail.com', 'user@1', 401),
    ('user1@gmail.com', 'wrongpassword', 401),
    ('user1', 'user@1', 401),
    (None, 'user@1', 422),
    ('user1@gmail.com', None, 422),
    (None, None, 422)
  ]
)
def test_incorrect_login(client, test_user, email, password, status_code):
  res = client.post('/login', data={'username': email, 'password': password})

  assert res.status_code == status_code
