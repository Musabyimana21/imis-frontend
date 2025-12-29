import psycopg2

conn = psycopg2.connect('postgresql://postgres:password123@localhost:5432/imis')
cur = conn.cursor()

cur.execute("SELECT id, title, category, primary_image_url FROM items LIMIT 10")
items = cur.fetchall()

print("Current items in database:")
for item in items:
    print(f"ID: {item[0]}, Title: {item[1]}, Category: {item[2]}, Image: {item[3]}")

conn.close()