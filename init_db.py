import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to default postgres database to create our db
        conn = psycopg2.connect(
            user=os.getenv("POSTGRES_USER", "concert_user"),
            password=os.getenv("POSTGRES_PASSWORD", "giannis34%"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            dbname="postgres"  # Connect to default admin DB
        )
        conn.autocommit = True
        cursor = conn.cursor()

        dbname = os.getenv("POSTGRES_DB", "theatre_db")

        # Check if database exists
        cursor.execute(
            sql.SQL("SELECT 1 FROM pg_database WHERE datname = {}")
            .format(sql.Literal(dbname))
        )

        if not cursor.fetchone():
            cursor.execute(
                sql.SQL("CREATE DATABASE {}")
                .format(sql.Identifier(dbname))
            )
            logger.info(f"Database '{dbname}' created successfully")
        else:
            logger.info(f"Database '{dbname}' already exists")

        cursor.close()
        conn.close()

    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise



import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to default postgres database to create our db
        conn = psycopg2.connect(
            user=os.getenv("POSTGRES_USER", "concert_user"),
            password=os.getenv("POSTGRES_PASSWORD", "giannis34%"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            dbname="postgres"  # Connect to default admin DB
        )
        conn.autocommit = True
        cursor = conn.cursor()

        dbname = os.getenv("POSTGRES_DB", "theatre_db")

        # Check if database exists
        cursor.execute(
            sql.SQL("SELECT 1 FROM pg_database WHERE datname = {}")
            .format(sql.Literal(dbname))
        )

        if not cursor.fetchone():
            cursor.execute(
                sql.SQL("CREATE DATABASE {}")
                .format(sql.Identifier(dbname))
            )
            logger.info(f"Database '{dbname}' created successfully")
        else:
            logger.info(f"Database '{dbname}' already exists")

        cursor.close()
        conn.close()

    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise


def create_tables():
    """Create all tables in the database in proper order."""
    try:
        conn = psycopg2.connect(
            user=os.getenv("POSTGRES_USER", "concert_user"),
            password=os.getenv("POSTGRES_PASSWORD", "giannis34%"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            dbname=os.getenv("POSTGRES_DB", "theatre_db")
        )
        cursor = conn.cursor()

        # Create 'actors' table first
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS actors (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            bio TEXT,
            birth_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Create 'customers' table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            phone VARCHAR(50),
            is_active BOOLEAN DEFAULT TRUE,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Create 'directors' table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS directors (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            bio TEXT,
            birth_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Create 'plays' table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS plays (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            genre VARCHAR(100),
            description TEXT,
            duration INTEGER,
            director_id INTEGER REFERENCES directors(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Create 'showtimes' table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS showtimes (
            id SERIAL PRIMARY KEY,
            play_id INTEGER REFERENCES plays(id),
            datetime TIMESTAMP NOT NULL,
            venue VARCHAR(255) NOT NULL,
            available_seats INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Create 'tickets' table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id SERIAL PRIMARY KEY,
            showtime_id INTEGER REFERENCES showtimes(id),
            customer_id INTEGER REFERENCES customers(id),
            seat_number VARCHAR(20) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (showtime_id, seat_number)
        )
        """)

        # Create 'play_actors' junction table **after** 'actors' and 'plays' exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS play_actors (
            play_id INTEGER REFERENCES plays(id),
            actor_id INTEGER REFERENCES actors(id),
            PRIMARY KEY (play_id, actor_id)
        )
        """)

        conn.commit()
        logger.info("All tables created successfully.")

    except Exception as e:
        conn.rollback()
        logger.error(f"Error creating tables: {e}")
        raise
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_database()
    create_tables()
