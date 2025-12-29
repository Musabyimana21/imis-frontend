"""
Reset production database - Run this on Render console
"""
from app.core.database import engine, Base
from app.models.enhanced_models import User, AnonymousItem
from app.core.security import get_password_hash

# Drop all tables
Base.metadata.drop_all(bind=engine)
print("✅ Dropped all tables")

# Create all tables
Base.metadata.create_all(bind=engine)
print("✅ Created all tables")

# Create admin user
from app.core.database import SessionLocal
db = SessionLocal()

admin = User(
    email="admin@imis.rw",
    hashed_password=get_password_hash("admin123"),
    full_name="Admin User",
    phone="250788000000",
    role="admin",
    is_verified=True
)
db.add(admin)
db.commit()
print("✅ Created admin user: admin@imis.rw / admin123")

db.close()
print("✅ Database reset complete!")
