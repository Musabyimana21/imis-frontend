import psycopg2

conn = psycopg2.connect('postgresql://postgres:password123@localhost:5432/imis')
cur = conn.cursor()
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'items';")
columns = [row[0] for row in cur.fetchall()]
print("Items table columns:", columns)
conn.close()