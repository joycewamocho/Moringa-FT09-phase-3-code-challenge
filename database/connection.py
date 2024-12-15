import sqlite3

DATABASE_NAME = './database/magazine.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./database/magazine.db"  # Ensure this is the correct path

# Define the base class for models to inherit from
Base = declarative_base()

# Initialize the database connection
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This function creates all tables
def init_db():
    Base.metadata.create_all(bind=engine)

