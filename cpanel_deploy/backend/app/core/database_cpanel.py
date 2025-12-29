from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os

# Configure database connection for cPanel MySQL
if "mysql" in settings.DATABASE_URL:
    # MySQL configuration for cPanel
    connect_args = {
        "charset": "utf8mb4",
        "connect_timeout": 60
    }
elif "sqlite" in settings.DATABASE_URL:
    # SQLite configuration
    connect_args = {"check_same_thread": False}
elif "postgresql" in settings.DATABASE_URL:
    # PostgreSQL configuration
    connect_args = {
        "sslmode": "disable",
        "connect_timeout": 60
    }
else:
    connect_args = {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_timeout=60,
    max_overflow=10,
    echo=False  # Set to True for debugging
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()