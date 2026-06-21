import sqlite3

conn = sqlite3.connect("tea_house.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO teas
(tea_name,price,description)
VALUES
('Green Tea',5.99,'Fresh Organic Green Tea')
""")

cursor.execute("""
INSERT INTO teas
(tea_name,price,description)
VALUES
('Black Tea',6.99,'Premium Black Tea')
""")


cursor.execute("""
INSERT INTO teas
(tea_name,price,description)
VALUES
('Milk Tea',7.99,'Creamy Milk Tea')
""")

conn.commit()
conn.close()

print("Tea Added Successfully")