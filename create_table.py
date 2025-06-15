import os
import psycopg2
from psycopg2 import sql
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database():
    try:
        conn = psycopg2.connect(
            user=os.getenv("POSTGRES_USER", "concert_user"),
            password=os.getenv("POSTGRES_PASSWORD", "giannis34%"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            dbname="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        dbname = os.getenv("POSTGRES_DB", "theatre_db")
        cursor.execute(
            sql.SQL("SELECT 1 FROM pg_database WHERE datname = {}")
            .format(sql.Literal(dbname))
        )

        if not cursor.fetchone():
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname))
            )
            logging.info(f"Database '{dbname}' created successfully")
        else:
            logging.info(f"Database '{dbname}' already exists")
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise

def create_tables():
    try:
        conn = psycopg2.connect(
            user=os.getenv("POSTGRES_USER", "concert_user"),
            password=os.getenv("POSTGRES_PASSWORD", "giannis34%"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            dbname=os.getenv("POSTGRES_DB", "theatre_db")
        )
        cursor = conn.cursor()

        # Create tables here...
        # (Include the table creation SQL commands as shown earlier)

        # Example for actors table:
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
        # Repeat for other tables...
        # ...

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