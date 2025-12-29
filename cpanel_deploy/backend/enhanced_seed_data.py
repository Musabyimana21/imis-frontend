#!/usr/bin/env python3
"""
Enhanced Seed Data Script for IMIS
Creates comprehensive test data including users, items, matches, messages, and payments
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

def create_enhanced_seed_data():
    """Create comprehensive seed data for testing"""
    
    # Get database session
    db = Session(bind=engine)
    
    try:
        print("🌱 Creating enhanced seed data for IMIS...")
        
        # 1. Create System Settings
        print("📋 Creating system settings...")
        settings = [
            ("unlock_fee", "1000.0", "Fee to unlock contact information (RWF)"),
            ("commission_rate", "0.10", "Commission rate (10%)"),
            ("max_distance_km", "50", "Maximum matching distance in kilometers"),
            ("min_similarity_threshold", "0.3", "Minimum similarity threshold for matching"),
            ("text_weight", "0.7", "Weight for text similarity in matching"),
            ("location_weight", "0.3", "Weight for location proximity in matching"),
            ("system_email", "gaudencemusabyimana21@gmail.com", "System email address"),
            ("support_phone", "+250780460621", "Support phone number"),
            ("maintenance_mode", "false", "System maintenance mode"),
            ("max_items_per_user", "50", "Maximum items per user")
        ]
        
        for key, value, description in settings:
            existing = db.query(SystemSettings).filter(SystemSettings.key == key).first()
            if not existing:
                setting = SystemSettings(key=key, value=value, description=description)
                db.add(setting)
        
        # 2. Create Test Users
        print("👥 Creating test users...")
        users_data = [
            {
                "email": "admin@imis.rw",
                "password": "admin123",
                "full_name": "MUSABYIMANA Gaudence",
                "phone": "+250780460621",
                "role": UserRole.ADMIN,
                "bio": "System administrator for IMIS platform",
                "location": "Kigali, Rwanda",
                "is_verified": True
            },
            {
                "email": "loser@imis.rw", 
                "password": "lost123",
                "full_name": "Jean Mugabo",
                "phone": "+250780460622",
                "role": UserRole.USER,
                "bio": "Lost my phone at Kigali Market",
                "location": "Kigali City",
                "is_verified": True
            },
            {
                "email": "finder@imis.rw",
                "password": "found123", 
                "full_name": "Marie Uwase",
                "phone": "+250780460623",
                "role": UserRole.USER,
                "bio": "Found several items, happy to help reunite them",
                "location": "Kimironko",
                "is_verified": True
            },
            {
                "email": "user1@imis.rw",
                "password": "password123",
                "full_name": "User One",
                "phone": "+250780460624",
                "role": UserRole.USER,
                "bio": "Regular user of the platform",
                "location": "Nyamirambo",
                "is_verified": True
            },
            {
                "email": "alice@imis.rw",
                "password": "alice123",
                "full_name": "Alice Mukamana",
                "phone": "+250780460625",
                "role": UserRole.USER,
                "bio": "University student, lost my laptop",
                "location": "Remera",
                "is_verified": True
            },
            {
                "email": "bob@imis.rw",
                "password": "bob123",
                "full_name": "Bob Nkurunziza",
                "phone": "+250780460626",
                "role": UserRole.USER,
                "bio": "Taxi driver, often find items in my car",
                "location": "Kicukiro",
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
        
        # 3. Create Sample Items
        print("📱 Creating sample items...")
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
            {
                "user_email": "alice@imis.rw",
                "title": "Dell Laptop",
                "description": "Lost my silver Dell laptop at University of Rwanda. Has stickers on the back and contains important thesis work.",
                "category": ItemCategory.ELECTRONICS,
                "status": ItemStatus.LOST,
                "location_name": "University of Rwanda, Gikondo",
                "latitude": -1.9659,
                "longitude": 30.0588,
                "brand": "Dell",
                "model": "Inspiron 15",
                "color": "Silver",
                "distinctive_features": "Multiple stickers on back cover, thesis files",
                "reward_amount": 100000.0,
                "date_lost_found": datetime.utcnow() - timedelta(days=5)
            },
            {
                "user_email": "user1@imis.rw",
                "title": "Brown Leather Wallet",
                "description": "Lost brown leather wallet with ID cards and some cash near Nyamirambo market.",
                "category": ItemCategory.WALLET,
                "status": ItemStatus.LOST,
                "location_name": "Nyamirambo Market",
                "latitude": -1.9706,
                "longitude": 30.0394,
                "brand": "Leather",
                "color": "Brown",
                "distinctive_features": "Contains ID card, driving license, some cash",
                "reward_amount": 20000.0,
                "date_lost_found": datetime.utcnow() - timedelta(days=1)
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
            },
            {
                "user_email": "bob@imis.rw",
                "title": "Silver Laptop",
                "description": "Found a silver laptop in my taxi. Has some stickers and seems to belong to a student.",
                "category": ItemCategory.ELECTRONICS,
                "status": ItemStatus.FOUND,
                "location_name": "Remera Taxi Park",
                "latitude": -1.9441,
                "longitude": 30.0619,
                "brand": "Dell",
                "color": "Silver",
                "distinctive_features": "Student stickers, academic files visible",
                "date_lost_found": datetime.utcnow() - timedelta(days=3)
            },
            {
                "user_email": "finder@imis.rw",
                "title": "Brown Wallet",
                "description": "Found a brown leather wallet near the market. Contains some cards and cash.",
                "category": ItemCategory.WALLET,
                "status": ItemStatus.FOUND,
                "location_name": "Nyamirambo Market Area",
                "latitude": -1.9700,
                "longitude": 30.0400,
                "color": "Brown",
                "distinctive_features": "Leather material, contains ID cards",
                "date_lost_found": datetime.utcnow() - timedelta(hours=12)
            },
            {
                "user_email": "bob@imis.rw",
                "title": "Car Keys with Toyota Keychain",
                "description": "Found car keys with Toyota keychain and house keys in my taxi.",
                "category": ItemCategory.KEYS,
                "status": ItemStatus.FOUND,
                "location_name": "Kigali City Center",
                "latitude": -1.9441,
                "longitude": 30.0619,
                "brand": "Toyota",
                "distinctive_features": "Toyota keychain, multiple keys including house keys",
                "date_lost_found": datetime.utcnow() - timedelta(hours=6)
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
        
        # 4. Create Sample Messages
        print("💬 Creating sample messages...")
        messages_data = [
            {
                "sender_email": "loser@imis.rw",
                "receiver_email": "finder@imis.rw", 
                "item_title": "Black iPhone with Blue Case",
                "content": "Hi! I think this might be my phone. I lost a black iPhone with blue case at Kigali Market. Can you tell me more details?",
                "created_at": datetime.utcnow() - timedelta(hours=2)
            },
            {
                "sender_email": "finder@imis.rw",
                "receiver_email": "loser@imis.rw",
                "item_title": "Black iPhone with Blue Case", 
                "content": "Hello! Yes, I found it near Kimironko Market. It has a cracked screen protector. Can you describe any other distinctive features?",
                "created_at": datetime.utcnow() - timedelta(hours=1, minutes=45)
            },
            {
                "sender_email": "loser@imis.rw",
                "receiver_email": "finder@imis.rw",
                "item_title": "Black iPhone with Blue Case",
                "content": "Yes! That's definitely mine. It has family photos and the wallpaper is a picture of my daughter. Can we meet to verify?",
                "created_at": datetime.utcnow() - timedelta(hours=1, minutes=30)
            },
            {
                "sender_email": "alice@imis.rw",
                "receiver_email": "bob@imis.rw",
                "item_title": "Silver Laptop",
                "content": "Hi! I lost my laptop and saw your found item. It's a Dell with academic stickers. Is this mine?",
                "created_at": datetime.utcnow() - timedelta(hours=3)
            }
        ]
        
        for msg_data in messages_data:
            sender = users[msg_data["sender_email"]]
            receiver = users[msg_data["receiver_email"]]
            item = items[msg_data["item_title"]]
            
            message = Message(
                sender_id=sender.id,
                receiver_id=receiver.id,
                item_id=item.id,
                content=msg_data["content"],
                created_at=msg_data["created_at"],
                is_read=random.choice([True, False])
            )
            db.add(message)
            
            # Update item message count
            item.message_count += 1
        
        # 5. Create Sample Payments
        print("💰 Creating sample payments...")
        payments_data = [
            {
                "user_email": "loser@imis.rw",
                "item_title": "Black iPhone with Blue Case",
                "amount": 1000.0,
                "payment_method": "mtn_momo",
                "phone_number": "+250780460622",
                "status": PaymentStatus.COMPLETED,
                "completed_at": datetime.utcnow() - timedelta(hours=1)
            },
            {
                "user_email": "alice@imis.rw", 
                "item_title": "Silver Laptop",
                "amount": 1000.0,
                "payment_method": "airtel_money",
                "phone_number": "+250780460625",
                "status": PaymentStatus.PENDING
            }
        ]
        
        for payment_data in payments_data:
            user = users[payment_data["user_email"]]
            item = items[payment_data["item_title"]]
            
            payment = Payment(
                user_id=user.id,
                item_id=item.id,
                amount=payment_data["amount"],
                payment_method=payment_data["payment_method"],
                phone_number=payment_data["phone_number"],
                status=payment_data["status"],
                transaction_id=f"IMIS_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}",
                description=f"Unlock contact for item: {item.title}",
                created_at=datetime.utcnow() - timedelta(hours=2),
                completed_at=payment_data.get("completed_at")
            )
            db.add(payment)
            db.flush()
            
            # Create commission if payment completed
            if payment.status == PaymentStatus.COMPLETED:
                commission = Commission(
                    item_id=item.id,
                    payment_id=payment.id,
                    amount=payment.amount * 0.10,
                    rate=0.10,
                    status="pending"
                )
                db.add(commission)
        
        # 6. Create Sample Reviews
        print("⭐ Creating sample reviews...")
        reviews_data = [
            {
                "reviewer_email": "loser@imis.rw",
                "reviewed_email": "finder@imis.rw",
                "item_title": "Black iPhone with Blue Case",
                "rating": 5,
                "comment": "Amazing! Marie helped me get my phone back. Very honest and helpful person. Highly recommend!"
            },
            {
                "reviewer_email": "finder@imis.rw",
                "reviewed_email": "loser@imis.rw", 
                "item_title": "Black iPhone with Blue Case",
                "rating": 5,
                "comment": "Jean was very polite and grateful. Easy transaction and verification process."
            }
        ]
        
        for review_data in reviews_data:
            reviewer = users[review_data["reviewer_email"]]
            reviewed = users[review_data["reviewed_email"]]
            item = items[review_data["item_title"]]
            
            review = Review(
                reviewer_id=reviewer.id,
                reviewed_id=reviewed.id,
                item_id=item.id,
                rating=review_data["rating"],
                comment=review_data["comment"]
            )
            db.add(review)
        
        # 7. Create Sample Notifications
        print("🔔 Creating sample notifications...")
        notifications_data = [
            {
                "user_email": "loser@imis.rw",
                "title": "🎉 High Confidence Match Found!",
                "message": "We found a high-confidence match for your lost item 'Black iPhone 13 Pro'",
                "type": "match",
                "item_title": "Black iPhone 13 Pro"
            },
            {
                "user_email": "finder@imis.rw",
                "title": "💬 New Message",
                "message": "You have a new message from Jean Mugabo about 'Black iPhone with Blue Case'",
                "type": "message",
                "item_title": "Black iPhone with Blue Case"
            },
            {
                "user_email": "loser@imis.rw",
                "title": "💰 Payment Successful!",
                "message": "Your payment of 1,000 RWF has been confirmed. You can now contact the finder.",
                "type": "payment",
                "item_title": "Black iPhone with Blue Case"
            }
        ]
        
        for notif_data in notifications_data:
            user = users[notif_data["user_email"]]
            item = items.get(notif_data["item_title"])
            
            notification = Notification(
                user_id=user.id,
                title=notif_data["title"],
                message=notif_data["message"],
                type=notif_data["type"],
                item_id=item.id if item else None,
                is_read=random.choice([True, False]),
                created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 24))
            )
            db.add(notification)
        
        # Commit all changes
        db.commit()
        
        print("✅ Enhanced seed data created successfully!")
        print("\n📊 Summary:")
        print(f"   👥 Users: {len(users_data)}")
        print(f"   📱 Items: {len(items_data)}")
        print(f"   💬 Messages: {len(messages_data)}")
        print(f"   💰 Payments: {len(payments_data)}")
        print(f"   ⭐ Reviews: {len(reviews_data)}")
        print(f"   🔔 Notifications: {len(notifications_data)}")
        print(f"   ⚙️  Settings: {len(settings)}")
        
        print("\n🔐 Test Credentials:")
        print("   Admin:  admin@imis.rw / admin123")
        print("   Loser:  loser@imis.rw / lost123")
        print("   Finder: finder@imis.rw / found123")
        print("   User:   user1@imis.rw / password123")
        print("   Alice:  alice@imis.rw / alice123")
        print("   Bob:    bob@imis.rw / bob123")
        
        print("\n🚀 Ready to test!")
        print("   Frontend: http://localhost:5173")
        print("   Backend:  http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Error creating seed data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_enhanced_seed_data()