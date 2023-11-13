from fastapi import Depends, HTTPException, status, APIRouter
from .. import models, schemas, database
from ..oauth2 import get_current_user
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/vote",
  tags=['votes']
)


@router.post("/")
def vote(
  vote: schemas.Vote, 
  user: models.User = Depends(get_current_user),
  db: Session = Depends(database.get_db),
):

  post = db.query(models.Post).where(models.Post.id == vote.post_id).first()

  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post {vote.post_id} does not exist")
  

  vote_query = db.query(models.Vote).where(models.Vote.post_id == vote.post_id, models.Vote.user_id == user.id)

  found_vote = vote_query.first()

  if vote.direction == 1:
    if found_vote:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The post {vote.post_id} is already upvoted by user {user.id}")
    
    vote_mod = models.Vote(post_id=vote.post_id, user_id=user.id)
    db.add(vote_mod)
    db.commit()
    db.refresh(vote_mod)

    return vote_mod

  else:
    if not found_vote:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The vote does not exist")
    
    vote_query.delete(synchronize_session=False)
    db.commit()

    return {'detail': 'vote removed'}



  
