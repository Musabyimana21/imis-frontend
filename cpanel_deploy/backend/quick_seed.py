from app.core.database import SessionLocal
from app.models.enhanced_models import User, Item
from app.core.security import get_password_hash
from datetime import datetime

db = SessionLocal()

# Check if users exist
admin = db.query(User).filter(User.email == "admin@imis.rw").first()
if not admin:
    admin = User(
        email="admin@imis.rw",
        full_name="Admin User",
        phone="250788000001",
        hashed_password=get_password_hash("admin123"),
        is_active=True,
        role="ADMIN"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print("Admin user created")
else:
    print("Admin user already exists")

user = db.query(User).filter(User.email == "user@imis.rw").first()
if not user:
    user = User(
        email="user@imis.rw",
        full_name="Test User",
        phone="250788000002",
        hashed_password=get_password_hash("user123"),
        is_active=True,
        role="USER"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print("Test user created")
else:
    print("Test user already exists")

# Create items
items = [
    Item(
        title="Lost iPhone 14 Pro",
        description="Black iPhone 14 Pro lost near Kigali Convention Centre",
        category="Electronics",
        status="LOST",
        location_name="Kigali Convention Centre",
        latitude=-1.9536,
        longitude=30.0927,
        user_id=user.id,
        contact_method="both",
        is_active=True,
        date_lost_found=datetime.now()
    ),
    Item(
        title="Found Wallet with ID",
        description="Brown leather wallet found at City Market",
        category="Documents",
        status="FOUND",
        location_name="City Market, Kigali",
        latitude=-1.9500,
        longitude=30.0588,
        user_id=admin.id,
        contact_method="phone",
        is_active=True,
        date_lost_found=datetime.now()
    ),
    Item(
        title="Lost Car Keys",
        description="Toyota car keys with red keychain",
        category="Keys",
        status="LOST",
        location_name="Kimironko Market",
        latitude=-1.9447,
        longitude=30.1265,
        user_id=user.id,
        contact_method="phone",
        is_active=True,
        date_lost_found=datetime.now()
    ),
    Item(
        title="Found Laptop Bag",
        description="Black Dell laptop bag found at bus station",
        category="Electronics",
        status="FOUND",
        location_name="Nyabugogo Bus Station",
        latitude=-1.9706,
        longitude=30.0444,
        user_id=admin.id,
        contact_method="both",
        is_active=True,
        date_lost_found=datetime.now()
    ),
    Item(
        title="Lost Passport",
        description="Rwandan passport lost near airport",
        category="Documents",
        status="LOST",
        location_name="Kigali International Airport",
        latitude=-1.9686,
        longitude=30.1395,
        user_id=user.id,
        contact_method="email",
        is_active=True,
        date_lost_found=datetime.now()
    )
]

for item in items:
    db.add(item)

db.commit()
print(f"Created {len(items)} items successfully!")
db.close()
