#!/usr/bin/env python3
"""
Quick database connection test
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    """Test database connection"""
    print("Testing database connection...")
    
    try:
        # Test PostgreSQL server connection
        conn = psycopg2.connect(
            host="localhost",
            port="5432", 
            user="postgres",
            password="password123"
        )
        print("PostgreSQL server connection: OK")
        conn.close()
        
        # Test IMIS database connection
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres", 
            password="password123",
            database="imis"
        )
        print("IMIS database connection: OK")
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    if success:
        print("\nDatabase connection is working!")
    else:
        print("\nDatabase connection failed!")
        print("Try running: RESET_PG18_PASSWORD.bat")