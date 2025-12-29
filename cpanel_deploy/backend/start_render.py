#!/usr/bin/env python3
"""
Render.com startup script for IMIS Backend
Ensures proper database initialization and health checks
"""

import os
import sys
import time
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_database(database_url, max_retries=30, delay=2):
    """Wait for database to be available"""
    logger.info("Waiting for database connection...")
    
    for attempt in range(max_retries):
        try:
            engine = create_engine(database_url)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection successful!")
            return True
        except OperationalError as e:
            logger.warning(f"Database connection attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                logger.error("Failed to connect to database after all retries")
                return False
    return False

def initialize_database():
    """Initialize database tables"""
    try:
        from app.core.database import engine, Base
        from app.models import enhanced_models
        
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return False

def main():
    """Main startup function"""
    logger.info("Starting IMIS Backend initialization...")
    
    # Check required environment variables
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        logger.error("DATABASE_URL environment variable is required")
        sys.exit(1)
    
    # Wait for database
    if not wait_for_database(database_url):
        logger.error("Database is not available")
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        logger.error("Failed to initialize database")
        sys.exit(1)
    
    logger.info("IMIS Backend initialization completed successfully!")
    
    # Start the application
    port = int(os.getenv('PORT', 10000))
    logger.info(f"Starting application on port {port}")
    
    os.system(f"gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:{port}")

if __name__ == "__main__":
    main()