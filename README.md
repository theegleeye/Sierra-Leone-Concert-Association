Sierra Leone Concert Association API

This project is a RESTful API built with FastAPI for managing concert-related data such as plays, actors, directors, showtimes, tickets, and customers. It includes authentication, search, pagination, and email notifications.



 Requirements

Before you begin, ensure you have the following installed:

- Python 3.10 or higher
- pip (Python package manager)
- Git (optional, for cloning the repo)



 Project Setup Instructions

 Clone the Repository (or download the ZIP file)

 bash
git clone https://github.com/your-username/concert-api.git
cd concert-api

Create virtual environment
python -m venv venv

 Activate it On Windows: venv\Scripts\activate

 project dependencies:
pip install -r requirements.txt

Set Up Environment Variables:
DATABASE_URL=sqlite:///./concert.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_email_password

Run Database (PostgreSQL):
alembic upgrade head

Start the FastAPI Server:
uvicorn main:app --reload




