import sqlite3

conn = sqlite3.connect('sales.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
  OrderID INTEGER,
  Date TEXT,
  Product TEXT,
  Category TEXT,
  Quantity INTEGER,
  Price REAL,
  Revenue REAL
)
''')

sample_data = [
    (1, '2025-09-15', 'Widget', 'Gadgets', 10, 20.0, 200.0),
    (2, '2025-09-15', 'Gizmo', 'Gadgets', 5, 30.0, 150.0),
    (3, '2025-09-16', 'Doodad', 'Accessories', 8, 15.0, 120.0),
    (4, '2025-09-17', 'Thingamajig', 'Accessories', 3, 25.0, 75.0),
    (5, '2025-09-18', 'Widget', 'Gadgets', 7, 20.0, 140.0),
]

cursor.executemany('INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?)', sample_data)

conn.commit()
conn.close()

print("Sales database and sample data created successfully.")
