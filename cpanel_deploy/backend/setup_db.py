#!/usr/bin/env python3
"""
Simple database setup script
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Create database if it doesn't exist"""
    print("Setting up database...")
    
    try:
        # Connect to PostgreSQL server (not specific database)
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="password123"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='imis'")
        exists = cursor.fetchone()
        
        if not exists:
            print("Creating database 'imis'...")
            cursor.execute("CREATE DATABASE imis")
            print("Database 'imis' created!")
        else:
            print("Database 'imis' already exists!")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        return False

if __name__ == "__main__":
    success = create_database()
    if success:
        print("\nDatabase setup complete!")
    else:
        print("\nDatabase setup failed!")