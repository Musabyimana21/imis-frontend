#!/usr/bin/env python3
"""Create database tables"""

from app.core.database import engine, Base
from app.models import enhanced_models

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()