#!/usr/bin/env python3
"""
Simple Seed Data Script for IMIS
Creates test data without unicode characters
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import engine, get_db
from app.models.enhanced_models import (
    User, Item, Match, Message, Payment, Commission, Review, 
    Notification, SystemSettings, UserRole, ItemStatus, ItemCategory, PaymentStatus
)
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import random

def create_simple_seed_data():
    """Create simple seed data for testing"""
    
    # Get database session
    db = Session(bind=engine)
    
    try:
        print("Creating enhanced seed data for IMIS...")
        
        # 1. Create Test Users
        print("Creating test users...")
        users_data = [
            {
                "email": "admin@imis.rw",
                "password": "admin123",
                "full_name": "System Administrator",
                "phone": "+250788123456",
                "role": UserRole.ADMIN,
                "bio": "System administrator for IMIS platform",
                "location": "Kigali, Rwanda",
                "is_verified": True
            },
            {
                "email": "loser@imis.rw", 
                "password": "lost123",
                "full_name": "Jean Mugabo",
                "phone": "+250788234567",
                "role": UserRole.USER,
                "bio": "Lost my phone at Kigali Market",
                "location": "Kigali City",
                "is_verified": True
            },
            {
                "email": "finder@imis.rw",
                "password": "found123", 
                "full_name": "Marie Uwase",
                "phone": "+250788345678",
                "role": UserRole.USER,
                "bio": "Found several items, happy to help reunite them",
                "location": "Kimironko",
                "is_verified": True
            },
            {
                "email": "user1@imis.rw",
                "password": "password123",
                "full_name": "User One",
                "phone": "+250788456789",
                "role": UserRole.USER,
                "bio": "Regular user of the platform",
                "location": "Nyamirambo",
                "is_verified": True
            }
        ]
        
        users = {}
        for user_data in users_data:
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing_user:
                user = User(
                    email=user_data["email"],
                    hashed_password=get_password_hash(user_data["password"]),
                    full_name=user_data["full_name"],
                    phone=user_data["phone"],
                    role=user_data["role"],
                    bio=user_data["bio"],
                    location=user_data["location"],
                    is_verified=user_data["is_verified"],
                    last_login=datetime.utcnow() - timedelta(hours=random.randint(1, 48))
                )
                db.add(user)
                db.flush()
                users[user_data["email"]] = user
            else:
                users[user_data["email"]] = existing_user
        
        # 2. Create Sample Items
        print("Creating sample items...")
        items_data = [
            # Lost Items
            {
                "user_email": "loser@imis.rw",
                "title": "Black iPhone 13 Pro",
                "description": "Lost my black iPhone 13 Pro with blue case at Kigali City Market. Has a cracked screen protector and family photos. Very important to me!",
                "category": ItemCategory.PHONE,
                "status": ItemStatus.LOST,
                "location_name": "Kigali City Market",
                "latitude": -1.9536,
                "longitude": 30.0606,
                "brand": "Apple",
                "model": "iPhone 13 Pro",
                "color": "Black",
                "distinctive_features": "Blue case, cracked screen protector, family photos",
                "reward_amount": 50000.0,
                "date_lost_found": datetime.utcnow() - timedelta(days=2)
            },
            
            # Found Items
            {
                "user_email": "finder@imis.rw",
                "title": "Black iPhone with Blue Case",
                "description": "Found a black iPhone with blue protective case near Kimironko Market. Screen has some damage but phone seems to work.",
                "category": ItemCategory.PHONE,
                "status": ItemStatus.FOUND,
                "location_name": "Kimironko Market",
                "latitude": -1.9447,
                "longitude": 30.1131,
                "brand": "Apple",
                "color": "Black",
                "distinctive_features": "Blue protective case, damaged screen",
                "date_lost_found": datetime.utcnow() - timedelta(days=1)
            }
        ]
        
        items = {}
        for item_data in items_data:
            user = users[item_data["user_email"]]
            
            item = Item(
                user_id=user.id,
                title=item_data["title"],
                description=item_data["description"],
                category=item_data["category"],
                status=item_data["status"],
                location_name=item_data["location_name"],
                latitude=item_data["latitude"],
                longitude=item_data["longitude"],
                brand=item_data.get("brand"),
                model=item_data.get("model"),
                color=item_data.get("color"),
                distinctive_features=item_data.get("distinctive_features"),
                reward_amount=item_data.get("reward_amount", 0.0),
                date_lost_found=item_data["date_lost_found"],
                view_count=random.randint(5, 50),
                created_at=item_data["date_lost_found"] + timedelta(minutes=random.randint(1, 60))
            )
            
            # Generate text vector and keywords
            text_content = f"{item.title} {item.description} {item.brand or ''} {item.model or ''} {item.color or ''}"
            item.text_vector = text_content.lower()
            item.match_keywords = list(set(text_content.lower().split()))[:20]
            
            db.add(item)
            db.flush()
            items[item_data["title"]] = item
            
            # Update user statistics
            if item.status == ItemStatus.LOST:
                user.items_lost += 1
            else:
                user.items_found += 1
        
        # Commit all changes
        db.commit()
        
        print("Enhanced seed data created successfully!")
        print("\nSummary:")
        print(f"   Users: {len(users_data)}")
        print(f"   Items: {len(items_data)}")
        
        print("\nTest Credentials:")
        print("   Admin:  admin@imis.rw / admin123")
        print("   Loser:  loser@imis.rw / lost123")
        print("   Finder: finder@imis.rw / found123")
        print("   User:   user1@imis.rw / password123")
        
        print("\nReady to test!")
        print("   Frontend: http://localhost:5173")
        print("   Backend:  http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"Error creating seed data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_simple_seed_data()