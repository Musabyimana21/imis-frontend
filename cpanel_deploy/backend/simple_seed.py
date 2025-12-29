import psycopg2
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
]

FOUND_ITEMS = [
    {'title': 'iPhone 13', 'desc': 'Found black iPhone near market. Screen is cracked.', 'cat': 'phone'},
    {'title': 'Leather Wallet', 'desc': 'Found brown wallet with some cards inside.', 'cat': 'wallet'},
    {'title': 'Toyota Car Keys', 'desc': 'Found car keys with Toyota logo at parking lot.', 'cat': 'keys'},
    {'title': 'Nike Backpack', 'desc': 'Found blue backpack at bus station. Contains laptop.', 'cat': 'bag'},
]

SAMPLE_IMAGES = {
    'phone': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop',
    'wallet': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop',
    'keys': 'https://images.unsplash.com/photo-1582139329536-e7284fece509?w=400&h=300&fit=crop',
    'bag': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop',
    'documents': 'https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=400&h=300&fit=crop',
    'electronics': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400&h=300&fit=crop',
    'jewelry': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=300&fit=crop',
    'other': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop'
}

conn = psycopg2.connect('postgresql://postgres:password123@localhost:5432/imis')
cur = conn.cursor()

print("Creating users...")

# Create admin user
cur.execute("""
    INSERT INTO users (email, hashed_password, full_name, phone, role, created_at)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id
""", ('admin@imis.rw', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdXzgVjHUxrLW', 'MUSABYIMANA Gaudence', '+250780460621', 'ADMIN', datetime.utcnow()))

admin_id = cur.fetchone()[0]
print(f"Created admin user with ID: {admin_id}")

# Create regular users
user_ids = []
for i in range(1, 6):
    cur.execute("""
        INSERT INTO users (email, hashed_password, full_name, phone, role, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (f'user{i}@imis.rw', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdXzgVjHUxrLW', f'User {i}', f'+25078046{i:04d}', 'USER', datetime.utcnow()))
    
    user_id = cur.fetchone()[0]
    user_ids.append(user_id)
    print(f"Created user {i} with ID: {user_id}")

print("Creating items...")

# Create lost items
for item_data in LOST_ITEMS:
    location = random.choice(KIGALI_LOCATIONS)
    user_id = random.choice(user_ids)
    image_url = SAMPLE_IMAGES.get(item_data['cat'], SAMPLE_IMAGES['other'])
    
    cur.execute("""
        INSERT INTO items (user_id, title, description, category, status, location_name, 
                          latitude, longitude, primary_image_url, date_lost_found, created_at, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (user_id, item_data['title'], item_data['desc'], item_data['cat'].upper(), 'LOST',
          location['name'], location['lat'], location['lon'], image_url,
          datetime.utcnow() - timedelta(days=random.randint(1, 30)), datetime.utcnow(), True))

# Create found items
for item_data in FOUND_ITEMS:
    location = random.choice(KIGALI_LOCATIONS)
    user_id = random.choice(user_ids)
    image_url = SAMPLE_IMAGES.get(item_data['cat'], SAMPLE_IMAGES['other'])
    
    cur.execute("""
        INSERT INTO items (user_id, title, description, category, status, location_name, 
                          latitude, longitude, primary_image_url, date_lost_found, created_at, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (user_id, item_data['title'], item_data['desc'], item_data['cat'].upper(), 'FOUND',
          location['name'], location['lat'], location['lon'], image_url,
          datetime.utcnow() - timedelta(days=random.randint(1, 30)), datetime.utcnow(), True))

conn.commit()
conn.close()

print("Seeding complete!")
print("Test accounts:")
print("  Admin: admin@imis.rw / admin123")
print("  User:  user1@imis.rw / password123")