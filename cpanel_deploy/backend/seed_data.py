"""
Seed script to populate IMIS database with sample data
Run: python -m backend.seed_data
"""
from app.core.database import SessionLocal, engine
from app.models.enhanced_models import Base, User, Item, ItemStatus, UserRole
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import random

# Sample data
CATEGORIES = ['phone', 'wallet', 'keys', 'bag', 'documents', 'electronics', 'jewelry', 'other']

KIGALI_LOCATIONS = [
    {'name': 'Kigali City Market', 'lat': -1.9536, 'lon': 30.0606},
    {'name': 'Nyabugogo Bus Station', 'lat': -1.9403, 'lon': 30.0588},
    {'name': 'Kimironko Market', 'lat': -1.9447, 'lon': 30.1131},
    {'name': 'Kigali Convention Centre', 'lat': -1.9514, 'lon': 30.0944},
    {'name': 'University of Rwanda', 'lat': -1.9659, 'lon': 30.1044},
    {'name': 'Kigali International Airport', 'lat': -1.9686, 'lon': 30.1395},
    {'name': 'Remera', 'lat': -1.9578, 'lon': 30.1047},
    {'name': 'Nyamirambo', 'lat': -1.9789, 'lon': 30.0428}
]

LOST_ITEMS = [
    {'title': 'Black iPhone 13 Pro', 'desc': 'Black iPhone 13 Pro with cracked screen protector. Has blue case.', 'cat': 'phone'},
    {'title': 'Brown Leather Wallet', 'desc': 'Brown leather wallet containing ID card and some cash. Lost near market.', 'cat': 'wallet'},
    {'title': 'Car Keys with Toyota Logo', 'desc': 'Set of car keys with Toyota keychain and house keys attached.', 'cat': 'keys'},
    {'title': 'Blue Backpack', 'desc': 'Blue Nike backpack with laptop inside. Contains important documents.', 'cat': 'bag'},
    {'title': 'National ID Card', 'desc': 'National ID card in the name of Jean Baptiste. Lost at bus station.', 'cat': 'documents'},
    {'title': 'Silver MacBook Pro', 'desc': 'Silver MacBook Pro 13 inch with stickers on the lid.', 'cat': 'electronics'},
    {'title': 'Gold Wedding Ring', 'desc': 'Gold wedding ring with engraving inside. Sentimental value.', 'cat': 'jewelry'},
    {'title': 'Red Umbrella', 'desc': 'Red folding umbrella with wooden handle.', 'cat': 'other'},
]

FOUND_ITEMS = [
    {'title': 'iPhone 13', 'desc': 'Found black iPhone near market. Screen is cracked.', 'cat': 'phone'},
    {'title': 'Leather Wallet', 'desc': 'Found brown wallet with some cards inside.', 'cat': 'wallet'},
    {'title': 'Toyota Car Keys', 'desc': 'Found car keys with Toyota logo at parking lot.', 'cat': 'keys'},
    {'title': 'Nike Backpack', 'desc': 'Found blue backpack at bus station. Contains laptop.', 'cat': 'bag'},
    {'title': 'ID Card', 'desc': 'Found national ID card near Nyabugogo.', 'cat': 'documents'},
    {'title': 'MacBook Laptop', 'desc': 'Found silver laptop at cafe. Has stickers.', 'cat': 'electronics'},
    {'title': 'Wedding Ring', 'desc': 'Found gold ring in restroom. Has engraving.', 'cat': 'jewelry'},
    {'title': 'Umbrella', 'desc': 'Found red umbrella at restaurant.', 'cat': 'other'},
]

def create_users(db):
    """Create sample users"""
    users = []
    
    # Admin user
    admin = User(
        email='admin@imis.rw',
        hashed_password=get_password_hash('admin123'),
        full_name='MUSABYIMANA Gaudence',
        phone='+250780460621',
        role=UserRole.ADMIN
    )
    db.add(admin)
    users.append(admin)
    
    # Regular users
    for i in range(1, 11):
        user = User(
            email=f'user{i}@imis.rw',
            hashed_password=get_password_hash('password123'),
            full_name=f'User {i}',
            phone=f'+25078046{i:04d}',
            role=UserRole.USER
        )
        db.add(user)
        users.append(user)
    
    db.commit()
    print(f"✓ Created {len(users)} users")
    return users

def create_items(db, users):
    """Create sample lost and found items"""
    items = []
    
    # Create lost items
    for i, item_data in enumerate(LOST_ITEMS):
        location = random.choice(KIGALI_LOCATIONS)
        user = random.choice(users[1:])  # Skip admin
        
        item = Item(
            user_id=user.id,
            title=item_data['title'],
            description=item_data['desc'],
            category=item_data['cat'],
            status=ItemStatus.LOST,
            location_name=location['name'],
            latitude=location['lat'],
            longitude=location['lon'],
            date_lost_found=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            image_url='📦'
        )
        db.add(item)
        items.append(item)
    
    # Create found items
    for i, item_data in enumerate(FOUND_ITEMS):
        location = random.choice(KIGALI_LOCATIONS)
        user = random.choice(users[1:])  # Skip admin
        
        item = Item(
            user_id=user.id,
            title=item_data['title'],
            description=item_data['desc'],
            category=item_data['cat'],
            status=ItemStatus.FOUND,
            location_name=location['name'],
            latitude=location['lat'],
            longitude=location['lon'],
            date_lost_found=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            image_url='📦'
        )
        db.add(item)
        items.append(item)
    
    db.commit()
    print(f"✓ Created {len(items)} items ({len(LOST_ITEMS)} lost, {len(FOUND_ITEMS)} found)")
    return items

def main():
    """Main seed function"""
    print("\n" + "="*50)
    print("IMIS Database Seeding")
    print("="*50 + "\n")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables ready\n")
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"⚠ Database already has {existing_users} users")
            response = input("Do you want to continue? This will add more data (y/n): ")
            if response.lower() != 'y':
                print("Seeding cancelled")
                return
        
        # Seed data
        users = create_users(db)
        items = create_items(db, users)
        
        print("\n" + "="*50)
        print("Seeding Complete!")
        print("="*50)
        print(f"\nTest Accounts:")
        print(f"  Admin: admin@imis.rw / admin123")
        print(f"  User:  user1@imis.rw / password123")
        print(f"\nTotal Users: {len(users)}")
        print(f"Total Items: {len(items)}")
        print("\n" + "="*50 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
