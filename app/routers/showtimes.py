from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/showtimes", tags=["showtimes"])

# Create showtime
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Showtime)
def create_showtime(showtime: schemas.ShowtimeCreate, db: Session = Depends(get_db)):
    # Verify play exists
    play = db.query(models.Play).filter(models.Play.id == showtime.play_id).first()
    if not play:
        raise HTTPException(status_code=404, detail="Play not found")
    db_showtime = models.Showtime(**showtime.dict())
    db.add(db_showtime)
    db.commit()
    db.refresh(db_showtime)
    return db_showtime

# Get all showtimes
@router.get("/", response_model=List[schemas.Showtime])
def get_showtimes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Showtime).offset(skip).limit(limit).all()

# Get showtime by ID
@router.get("/{showtime_id}", response_model=schemas.Showtime)
def get_showtime(showtime_id: int, db: Session = Depends(get_db)):
    showtime = db.query(models.Showtime).filter(models.Showtime.id == showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")
    return showtime

# Update showtime
@router.put("/{showtime_id}", response_model=schemas.Showtime)
def update_showtime(showtime_id: int, showtime_data: schemas.ShowtimeCreate, db: Session = Depends(get_db)):
    showtime = db.query(models.Showtime).filter(models.Showtime.id == showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")
    # Verify play if play_id is being updated
    if showtime_data.play_id:
        play = db.query(models.Play).filter(models.Play.id == showtime_data.play_id).first()
        if not play:
            raise HTTPException(status_code=404, detail="Play not found")
    for field, value in showtime_data.dict().items():
        setattr(showtime, field, value)
    db.commit()
    db.refresh(showtime)
    return showtime

# Delete showtime
@router.delete("/{showtime_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_showtime(showtime_id: int, db: Session = Depends(get_db)):
    showtime = db.query(models.Showtime).filter(models.Showtime.id == showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")
    db.delete(showtime)
    db.commit()
    return None