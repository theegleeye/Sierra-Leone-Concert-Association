from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    tickets = relationship("Ticket", back_populates="customer")

class Director(Base):
    __tablename__ = "directors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    bio = Column(String)
    birth_date = Column(DateTime)
    plays = relationship("Play", back_populates="director")

class Play(Base):
    __tablename__ = "plays"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genre = Column(String)
    description = Column(String)
    duration = Column(Integer)
    director_id = Column(Integer, ForeignKey("directors.id"))
    director = relationship("Director", back_populates="plays")
    actors = relationship("Actor", secondary="play_actors", back_populates="plays")
    showtimes = relationship("Showtime", back_populates="play")

class Actor(Base):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    bio = Column(String)
    birth_date = Column(DateTime)
    plays = relationship("Play", secondary="play_actors", back_populates="actors")

class PlayActor(Base):
    __tablename__ = "play_actors"
    play_id = Column(Integer, ForeignKey("plays.id"), primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.id"), primary_key=True)

class Showtime(Base):
    __tablename__ = "showtimes"
    id = Column(Integer, primary_key=True, index=True)
    play_id = Column(Integer, ForeignKey("plays.id"))
    datetime = Column(DateTime)
    venue = Column(String)
    available_seats = Column(Integer)
    play = relationship("Play", back_populates="showtimes")
    tickets = relationship("Ticket", back_populates="showtime")

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    showtime_id = Column(Integer, ForeignKey("showtimes.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    seat_number = Column(String)
    price = Column(Float)
    booking_date = Column(DateTime, default=datetime.utcnow)
    showtime = relationship("Showtime", back_populates="tickets")
    customer = relationship("Customer", back_populates="tickets")