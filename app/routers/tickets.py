from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/tickets", tags=["tickets"])

# Create ticket
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Ticket)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    # Check if showtime exists
    showtime = db.query(models.Showtime).filter(models.Showtime.id == ticket.showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")
    # Check if customer exists
    customer = db.query(models.Customer).filter(models.Customer.id == ticket.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    # Check seat availability
    existing_ticket = db.query(models.Ticket).filter(
        models.Ticket.showtime_id == ticket.showtime_id,
        models.Ticket.seat_number == ticket.seat_number
    ).first()
    if existing_ticket:
        raise HTTPException(status_code=400, detail="Seat is already booked")
    # Create Ticket
    db_ticket = models.Ticket(**ticket.dict())
    db.add(db_ticket)
    # Decrement available seats
    showtime.available_seats -= 1
    db.add(showtime)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

# Get all tickets
@router.get("/", response_model=List[schemas.Ticket])
def get_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Ticket).offset(skip).limit(limit).all()

# Get ticket by ID
@router.get("/{ticket_id}", response_model=schemas.Ticket)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

# Update ticket
@router.put("/{ticket_id}", response_model=schemas.Ticket)
def update_ticket(ticket_id: int, ticket_data: schemas.TicketCreate, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    # Verify showtime if updated
    if ticket_data.showtime_id:
        showtime = db.query(models.Showtime).filter(models.Showtime.id == ticket_data.showtime_id).first()
        if not showtime:
            raise HTTPException(status_code=404, detail="Showtime not found")
    # Verify customer if updated
    if ticket_data.customer_id:
        customer = db.query(models.Customer).filter(models.Customer.id == ticket_data.customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
    # Check seat availability if seat_number changed
    if ticket_data.seat_number != ticket.seat_number:
        existing_ticket = db.query(models.Ticket).filter(
            models.Ticket.showtime_id == ticket.showtime_id,
            models.Ticket.seat_number == ticket_data.seat_number
        ).first()
        if existing_ticket:
            raise HTTPException(status_code=400, detail="Seat is already booked")
    # Update fields
    for field, value in ticket_data.dict().items():
        setattr(ticket, field, value)
    db.commit()
    db.refresh(ticket)
    return ticket

# Delete ticket
@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    # Increment seats on delete
    showtime = db.query(models.Showtime).filter(models.Showtime.id == ticket.showtime_id).first()
    if showtime:
        showtime.available_seats += 1
        db.add(showtime)
    db.delete(ticket)
    db.commit()
    return None