"""Test for posts"""
from app import schemas, models
import pytest

def _test_get_all_posts(client, test_posts):
  res = client.get('/posts/')

  # schema validation
  posts_lst = list(map(lambda p: schemas.PostOut(**p), res.json()))

  assert res.status_code == 200
  assert len(posts_lst) == len(test_posts)


def _test_get_one_post(client, test_posts):
  res = client.get(f'/posts/{test_posts[0].id}')

  assert res.status_code == 200
  assert res.json()['id'] == test_posts[0].id


def test_unauthorized_user_get_all_posts(client, test_posts):
  _test_get_all_posts(client, test_posts)


def test_authorized_user_get_all_posts(authorized_client, test_posts):
  _test_get_all_posts(authorized_client, test_posts)

def test_unauthorized_user_get_one_post(client, test_posts):
  _test_get_one_post(client, test_posts)


def test_authorized_user_get_one_post(authorized_client, test_posts):
  _test_get_one_post(authorized_client, test_posts)


@pytest.mark.parametrize(
  "query, expected_titles",[
    ("1st", {"1st post"}),
    ("2nd", {"2nd post"}),
    ("3rd", {"3rd post"}),
    ("post", {"1st post", "2nd post", "3rd post", "4th post"})
  ]
)
def test_filter_get_posts(client, test_posts, query, expected_titles):
  res = client.get('/posts/', params={'search': query})
  res_titles = {p['Post']['title'] for p in res.json()}
  assert res_titles == expected_titles


def test_get_one_post_not_exist(client, test_posts):
  res = client.get('/posts/9999')
  assert res.status_code == 404


def test_create_post(authorized_client, test_user):
  post_info = {'title': 'test create post', 'content': 'test content', 'published': False}
  res = authorized_client.post('/posts/', json=post_info)
  post_res = models.Post(**res.json())

  assert res.status_code == 201
  assert post_res.title == post_info['title']
  assert post_res.content == post_info['content']
  assert post_res.published == post_info['published']
  assert post_res.user_id == test_user['id']


def test_default_published_create_post(authorized_client, test_user):
  post_info = {'title': 'test create post', 'content': 'test content'}
  res = authorized_client.post('/posts/', json=post_info)
  post_res = models.Post(**res.json())

  assert res.status_code == 201
  assert post_res.title == post_info['title']
  assert post_res.content == post_info['content']
  assert post_res.user_id == test_user['id']
  assert post_res.published == True


def test_not_logged_in_user_delete_post(client, session, test_posts):
  res = client.delete('/posts/1')
  assert res.status_code == 401

  post_db = session.query(models.Post).where(models.Post.id == 1).first()
  assert post_db is not None


def test_not_owner_user_delete_post(authorized_client, session, test_posts):
  res = authorized_client.delete('/posts/4')
  assert res.status_code == 403

  post_db = session.query(models.Post).where(models.Post.id == 4).first()
  assert post_db is not None
  

def test_update_post(authorized_client, session, test_user, test_posts):

  upd_post_info = {'title': '1st post (upd)', 'content': '1st content (upd)'}
  res = authorized_client.put(
    '/posts/1', 
    json=upd_post_info
  )

  # schema validation
  upd_post = schemas.Post(**res.json())

  post_db = session.query(models.Post).filter(models.Post.id == 1).first()

  assert res.status_code == 200

  assert post_db.title == upd_post_info['title']
  assert post_db.content == upd_post_info['content']
  assert post_db.published == upd_post_info.get('published', True)
  assert post_db.user_id == test_user['id']


def test_not_owner_user_update_post(authorized_client, session, test_posts, test_user, test_user2):
  upd_post_info = {'title': '4th post (upd)', 'content': '4th content (upd)'}
  res = authorized_client.put(
    '/posts/4', 
    json=upd_post_info
  )

  assert res.status_code == 403

  post_db = session.query(models.Post).filter(models.Post.id == 4).first()

  orig_post_info = test_posts[3] # for id = 4

  assert post_db.title == orig_post_info.title
  assert post_db.content == orig_post_info.content
  assert post_db.published == orig_post_info.published
  assert post_db.user_id == test_user2['id']


  
