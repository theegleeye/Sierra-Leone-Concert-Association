from fastapi import FastAPI
from app.routers import actors, customers, directors, plays, showtimes, tickets
from app.utils import auth

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Sierra Leone Concert Management API"}

# Include routers
app.include_router(actors.router)
app.include_router(customers.router)
app.include_router(directors.router)
app.include_router(plays.router)
app.include_router(showtimes.router)
app.include_router(tickets.router)
app.include_router(auth.router)