import sqlite3

conn = sqlite3.connect('tea_house.db')
cursor = conn.cursor()

cursor.execute("""
INSERT INTO users(name,email,password)
VALUES(
    'Admin',
    'admin@gmail.com',
    'admin123'
)
""")

conn.commit()
conn.close()

print("Admin Created Successfully")