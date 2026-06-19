import sqlite3

conn = sqlite3.connect('tea_house.db')
cursor = conn.cursor()

# Users Table

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
email TEXT UNIQUE NOT NULL,
password TEXT NOT NULL
)
""")

# Products Table

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
id INTEGER PRIMARY KEY AUTOINCREMENT,
product_name TEXT NOT NULL,
category TEXT NOT NULL,
price REAL NOT NULL,
description TEXT NOT NULL
)
""")


# Tea Table

cursor.execute("""
CREATE TABLE IF NOT EXISTS teas(
id INTEGER PRIMARY KEY AUTOINCREMENT,
tea_name TEXT NOT NULL,
price REAL NOT NULL,
description TEXT NOT NULL
)
""")

# Cart Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS cart(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    tea_id INTEGER,
    quantity INTEGER DEFAULT 1
)
""")

# Orders Table

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
total_price REAL,
status TEXT,
order_date TEXT
)
""")


conn.commit()
conn.close()

print("Database Created Successfully")
