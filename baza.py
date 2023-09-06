import psycopg2

conn = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='zuzuna02',
    database='vezbam'
)

cur = conn.cursor()

cur.execute("SELECT email, password_hash FROM users")
rows = cur.fetchall()
for row in rows:
    print(row[0])

conn.commit()

cur.close()
conn.close()