import psycopg2

# Sample image URLs
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

# Get items without proper images
cur.execute("SELECT id, title, category FROM items WHERE primary_image_url IS NULL OR primary_image_url = ''")
items = cur.fetchall()

print(f"Found {len(items)} items to update")

for item_id, title, category in items:
    image_url = SAMPLE_IMAGES.get(category, SAMPLE_IMAGES['other'])
    cur.execute("UPDATE items SET primary_image_url = %s WHERE id = %s", (image_url, item_id))
    print(f"Updated: {title}")

conn.commit()
conn.close()
print("Done!")