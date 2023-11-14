"""Test for Votes"""
import pytest
from app import models

@pytest.fixture
def test_vote(test_user, test_posts, session):
  vote = models.Vote(**{'user_id': test_user['id'], 'post_id': test_posts[0].id})
  session.add(vote)
  session.commit()
  session.refresh(vote)

  return vote


def test_vote_on_post(authorized_client, test_posts):
  res = authorized_client.post('/vote', json={'post_id': test_posts[0].id, 'direction': 1})

  assert res.status_code == 201

def test_vote_twice_on_post(authorized_client, test_vote, test_posts):
  res = authorized_client.post('/vote', json={'post_id': test_posts[0].id, 'direction': 1})

  assert res.status_code == 409

def test_delete_vote(authorized_client, test_user, test_vote):
  res = authorized_client.post('/vote', json={'post_id': test_vote.post_id, 'direction': 0})

  assert res.status_code == 201


def test_delete_vote_not_exist(authorized_client, test_vote, test_posts):
  res = authorized_client.post('/vote', json={'post_id': test_posts[2].id, 'direction': 0})

  assert res.status_code == 404


def test_vote_post_not_exist(authorized_client, test_posts):
  res = authorized_client.post('/vote', json={'post_id': 9999, 'direction': 1})

  assert res.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
  res = client.post('/vote', json={'post_id': test_posts[0].id, 'direction': 1})

  assert res.status_code == 401