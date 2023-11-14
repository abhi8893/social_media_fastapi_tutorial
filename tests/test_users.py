"""Tests for users route"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
  res = client.get('/')
  assert res.json()['message'] == 'Welcome to my app!'
  assert res.status_code == 200
