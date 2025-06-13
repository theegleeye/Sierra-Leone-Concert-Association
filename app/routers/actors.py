from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/actors", tags=["actors"])

# Create Actor
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Actor)
def create_actor(actor: schemas.ActorCreate, db: Session = Depends(get_db)):
    db_actor = models.Actor(**actor.dict())
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor

# Get all actors
@router.get("/", response_model=List[schemas.Actor])
def get_actors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Actor).offset(skip).limit(limit).all()

# Get actor by ID
@router.get("/{actor_id}", response_model=schemas.Actor)
def get_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    return actor

# Update actor
@router.put("/{actor_id}", response_model=schemas.Actor)
def update_actor(actor_id: int, actor: schemas.ActorCreate, db: Session = Depends(get_db)):
    db_actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if not db_actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    for key, value in actor.dict().items():
        setattr(db_actor, key, value)
    db.commit()
    db.refresh(db_actor)
    return db_actor

# Delete actor
@router.delete("/{actor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    db.delete(actor)
    db.commit()
    return None