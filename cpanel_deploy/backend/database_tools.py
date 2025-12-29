#!/usr/bin/env python3
"""
IMIS Database Tools - Remote Database Access
Provides tools for managing remote database connections and operations
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class RemoteDBManager:
    def __init__(self, db_url=None):
        self.db_url = db_url or os.getenv('DATABASE_URL', 'postgresql://imis:imis123@localhost:5432/imis')
        self.engine = None
        
    def connect(self):
        """Establish remote database connection"""
        try:
            self.engine = create_engine(
                self.db_url,
                connect_args={"sslmode": "disable", "connect_timeout": 60},
                pool_pre_ping=True,
                pool_recycle=300
            )
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print(f"✅ Connected to remote database: {self.db_url.split('@')[1] if '@' in self.db_url else 'localhost'}")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def test_connection(self):
        """Test database connectivity"""
        if not self.engine:
            return self.connect()
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT version()"))
                version = result.fetchone()[0]
                print(f"✅ Database version: {version}")
                return True
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False
    
    def list_tables(self):
        """List all tables in database"""
        try:
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
            print(f"📋 Tables ({len(tables)}):")
            for table in tables:
                print(f"  - {table}")
            return tables
        except Exception as e:
            print(f"❌ Failed to list tables: {e}")
            return []
    
    def execute_query(self, query):
        """Execute SQL query"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                if result.returns_rows:
                    rows = result.fetchall()
                    print(f"✅ Query executed. Rows returned: {len(rows)}")
                    return rows
                else:
                    print("✅ Query executed successfully")
                    return True
        except Exception as e:
            print(f"❌ Query failed: {e}")
            return False

def setup_remote_db():
    """Interactive setup for remote database"""
    print("🔧 IMIS Remote Database Setup")
    print("=" * 40)
    
    # Get connection details
    host = input("Database Host (default: localhost): ").strip() or "localhost"
    port = input("Database Port (default: 5432): ").strip() or "5432"
    database = input("Database Name (default: imis): ").strip() or "imis"
    username = input("Username (default: imis): ").strip() or "imis"
    password = input("Password: ").strip()
    
    # Build connection URL
    db_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    
    # Test connection
    db_manager = RemoteDBManager(db_url)
    if db_manager.connect():
        # Save to .env file
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        with open(env_path, 'w') as f:
            f.write(f"DATABASE_URL={db_url}\n")
            f.write("SECRET_KEY=your-secret-key-change-in-production\n")
            f.write("ALGORITHM=HS256\n")
            f.write("ACCESS_TOKEN_EXPIRE_MINUTES=30\n")
        
        print(f"✅ Configuration saved to {env_path}")
        return db_manager
    else:
        print("❌ Setup failed")
        return None

def main():
    """Main database tools interface"""
    if len(sys.argv) < 2:
        print("Usage: python database_tools.py [setup|test|tables|query]")
        return
    
    command = sys.argv[1]
    
    if command == "setup":
        setup_remote_db()
    
    elif command == "test":
        db_manager = RemoteDBManager()
        db_manager.test_connection()
    
    elif command == "tables":
        db_manager = RemoteDBManager()
        if db_manager.connect():
            db_manager.list_tables()
    
    elif command == "query":
        if len(sys.argv) < 3:
            print("Usage: python database_tools.py query 'SELECT * FROM users LIMIT 5'")
            return
        
        query = sys.argv[2]
        db_manager = RemoteDBManager()
        if db_manager.connect():
            db_manager.execute_query(query)
    
    else:
        print("Unknown command. Use: setup, test, tables, or query")

if __name__ == "__main__":
    main()