#!/usr/bin/env python3
"""
Test script for Render PostgreSQL database connection
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

def test_database_connection(database_url):
    """Test database connection with proper SSL configuration"""
    print(f"Testing database connection...")
    print(f"Database URL: {database_url[:50]}...")
    
    try:
        # Configure engine with SSL settings for PostgreSQL
        if "postgresql" in database_url:
            connect_args = {
                "sslmode": "require",
                "connect_timeout": 30
            }
        else:
            connect_args = {}
            
        engine = create_engine(
            database_url,
            connect_args=connect_args,
            pool_pre_ping=True,
            pool_recycle=300
        )
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            print(f"Test query result: {result.fetchone()}")
            
        # Test creating a simple table
        with engine.connect() as connection:
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100)
                )
            """))
            connection.commit()
            print("✅ Table creation test successful!")
            
        return True
        
    except OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        if "SSL connection has been closed unexpectedly" in str(e):
            print("\n🔧 SSL Connection Issue Detected!")
            print("This usually means:")
            print("1. The database URL is incorrect")
            print("2. The database server is not accessible")
            print("3. SSL configuration is wrong")
            print("\nPlease check your DATABASE_URL in Render environment variables.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main test function"""
    print("🔍 Render Database Connection Test")
    print("=" * 50)
    
    # Get database URL from environment
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL environment variable not set!")
        print("\nTo test locally, set DATABASE_URL:")
        print("set DATABASE_URL=your_render_postgresql_url")
        return False
    
    if database_url == "<your-postgresql-internal-url-from-step-1.2>":
        print("❌ DATABASE_URL is still a placeholder!")
        print("Please replace with your actual Render PostgreSQL URL")
        return False
    
    success = test_database_connection(database_url)
    
    if success:
        print("\n🎉 All tests passed! Your database is ready.")
    else:
        print("\n❌ Database connection failed. Please check your configuration.")
        
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)