from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/plays", tags=["plays"])

# Create play
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Play)
def create_play(play: schemas.PlayCreate, db: Session = Depends(get_db)):
    # Verify director exists
    director = db.query(models.Director).filter(models.Director.id == play.director_id).first()
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    db_play = models.Play(**play.dict())
    db.add(db_play)
    db.commit()
    db.refresh(db_play)
    return db_play

# Get all plays
@router.get("/", response_model=List[schemas.Play])
def get_plays(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Play).offset(skip).limit(limit).all()

# Get play by ID
@router.get("/{play_id}", response_model=schemas.Play)
def get_play(play_id: int, db: Session = Depends(get_db)):
    play = db.query(models.Play).filter(models.Play.id == play_id).first()
    if not play:
        raise HTTPException(status_code=404, detail="Play not found")
    return play

# Update play
@router.put("/{play_id}", response_model=schemas.Play)
def update_play(play_id: int, play_data: schemas.PlayCreate, db: Session = Depends(get_db)):
    play = db.query(models.Play).filter(models.Play.id == play_id).first()
    if not play:
        raise HTTPException(status_code=404, detail="Play not found")
    for field, value in play_data.dict().items():
        setattr(play, field, value)
    db.commit()
    db.refresh(play)
    return play

# Delete play
@router.delete("/{play_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_play(play_id: int, db: Session = Depends(get_db)):
    play = db.query(models.Play).filter(models.Play.id == play_id).first()
    if not play:
        raise HTTPException(status_code=404, detail="Play not found")
    db.delete(play)
    db.commit()
    return None