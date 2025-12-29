"""Initialize database tables"""
import sys
sys.path.insert(0, '.')

from app.core.database import engine, Base
import app.models.enhanced_models  # Import to register models

print("Creating all database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully!")
