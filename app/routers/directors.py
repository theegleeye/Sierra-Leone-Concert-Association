from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/directors", tags=["directors"])

# Create director
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Director)
def create_director(director: schemas.DirectorCreate, db: Session = Depends(get_db)):
    db_director = models.Director(**director.dict())
    db.add(db_director)
    db.commit()
    db.refresh(db_director)
    return db_director

# Get all directors
@router.get("/", response_model=List[schemas.Director])
def get_directors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Director).offset(skip).limit(limit).all()

# Get director by ID
@router.get("/{director_id}", response_model=schemas.Director)
def get_director(director_id: int, db: Session = Depends(get_db)):
    director = db.query(models.Director).filter(models.Director.id == director_id).first()
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    return director

# Update director
@router.put("/{director_id}", response_model=schemas.Director)
def update_director(director_id: int, director_data: schemas.DirectorCreate, db: Session = Depends(get_db)):
    director = db.query(models.Director).filter(models.Director.id == director_id).first()
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    for field, value in director_data.dict().items():
        setattr(director, field, value)
    db.commit()
    db.refresh(director)
    return director

# Delete director
@router.delete("/{director_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_director(director_id: int, db: Session = Depends(get_db)):
    director = db.query(models.Director).filter(models.Director.id == director_id).first()
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    db.delete(director)
    db.commit()
    return None