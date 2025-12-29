"""
Fix image URLs in database - replace emoji placeholders with proper URLs
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password123@localhost:5432/imis")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sample image URLs (using placeholder service)
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

def fix_image_urls():
    """Update all items with proper image URLs"""
    db = SessionLocal()
    try:
        # Get all items that need image URL updates
        result = db.execute(text("SELECT id, title, category, primary_image_url FROM items WHERE primary_image_url IS NULL OR primary_image_url = '' OR primary_image_url = '📦'"))
        items = result.fetchall()
        updated_count = 0
        
        for item in items:
            item_id, title, category, current_url = item
            # Get image URL based on category
            new_image_url = SAMPLE_IMAGES.get(category, SAMPLE_IMAGES['other'])
            
            # Update both image fields
            db.execute(text("UPDATE items SET primary_image_url = :url, image_urls = :url WHERE id = :id"), 
                      {"url": new_image_url, "id": item_id})
            updated_count += 1
            print(f"Updated {title} -> {new_image_url}")
        
        db.commit()
        print(f"\n✓ Updated {updated_count} items with proper image URLs")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Fixing image URLs in database...")
    fix_image_urls()
    print("Done!")