from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from app.utils.auth import get_password_hash

router = APIRouter(prefix="/customers", tags=["customers"])

# Create customer
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    existing_customer = db.query(models.Customer).filter(models.Customer.email == customer.email).first()
    if existing_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(customer.password)
    db_customer = models.Customer(
        name=customer.name,
        email=customer.email,
        password=hashed_password,
        phone=customer.phone
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# Get all customers
@router.get("/", response_model=List[schemas.Customer])
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Customer).offset(skip).limit(limit).all()

# Get customer by ID
@router.get("/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

# Update customer
@router.put("/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, customer_data: schemas.CustomerCreate, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    # Check for email change
    if customer_data.email != customer.email:
        existing_customer = db.query(models.Customer).filter(
            models.Customer.email == customer_data.email,
            models.Customer.id != customer_id
        ).first()
        if existing_customer:
            raise HTTPException(status_code=400, detail="Email already registered by another user")
    # Update fields
    customer.name = customer_data.name
    customer.email = customer_data.email
    customer.phone = customer_data.phone
    # Update password if provided
    if customer_data.password:
        customer.password = get_password_hash(customer_data.password)
    db.commit()
    db.refresh(customer)
    return customer

# Delete customer
@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return None