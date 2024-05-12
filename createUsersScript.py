import mysql.connector
import random
from datetime import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="def",
    password="password",
    database="csit314_project"
)
cursor = conn.cursor()

for i in range(100):  # 100 rows
    username = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(5))
    password = username * 3
    name = username
    surname = username
    email = f"{username}@example.com"
    date_of_birth = datetime.strptime('2000-01-01', '%Y-%m-%d').date()
    address = username
    role = random.choice(['buyer', 'seller', 'agent'])
    membership_tier = 'basic'

    # Insert data into table
    query = "INSERT INTO useraccount (username, password, name, surname, email, date_of_birth, address, role, membership_tier) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (username, password, name, surname, email, date_of_birth, address, role, membership_tier)
    cursor.execute(query, data)

conn.commit()
conn.close()

print("data inserted successfully...")
