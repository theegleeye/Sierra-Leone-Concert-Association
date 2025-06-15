from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Play schemas
class PlayBase(BaseModel):
    title: str
    genre: str
    description: Optional[str] = None
    duration: int

class PlayCreate(PlayBase):
    director_id: int

class Play(PlayBase):
    id: int
    director_id: int

    class Config:
        form_attribute = True

# Actor schemas
class ActorBase(BaseModel):
    name: str
    bio: Optional[str] = None
    birth_date: Optional[datetime] = None

class ActorCreate(ActorBase):
    pass

class Actor(ActorBase):
    id: int

    class Config:
        form_attribute = True

# Director schemas
class DirectorBase(BaseModel):
    name: str
    bio: Optional[str] = None
    birth_date: Optional[datetime] = None

class DirectorCreate(DirectorBase):
    pass

class Director(DirectorBase):
    id: int

    class Config:
        form_attribute = True

# Showtime schemas
class ShowtimeBase(BaseModel):
    play_id: int
    datetime: datetime
    venue: str
    available_seats: int

class ShowtimeCreate(ShowtimeBase):
    pass

class Showtime(ShowtimeBase):
    id: int

    class Config:
        form_attribute = True

# Customer schemas
class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

class CustomerCreate(CustomerBase):
    password: str

class Customer(CustomerBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        form_attribute = True

# Ticket schemas
class TicketBase(BaseModel):
    showtime_id: int
    customer_id: int
    seat_number: str
    price: float

class TicketCreate(TicketBase):
    pass

class Ticket(TicketBase):
    id: int
    booking_date: datetime

    class Config:
        form_attribute= True