import sqlite3

# Connect to SQLite database file (creates file if not exists)
conn = sqlite3.connect('sales.db')

# Create a cursor to execute SQL commands
cur = conn.cursor()

# Create sales table with the required columns
create_table_query = """
CREATE TABLE IF NOT EXISTS sales (
  OrderID INTEGER PRIMARY KEY,
  Date TEXT,
  Product TEXT,
  Category TEXT,
  Quantity INTEGER,
  Price REAL,
  Revenue REAL
);
"""

cur.execute(create_table_query)

# Insert some sample sales rows
sample_data = [
    (1, '2025-01-01', 'Phone', 'Electronics', 3, 299.99, 899.97),
    (2, '2025-01-02', 'Laptop', 'Electronics', 2, 799.99, 1599.98),
    (3, '2025-01-03', 'Charger', 'Accessories', 5, 19.99, 99.95),
    (4, '2025-01-04', 'Tablet', 'Computers', 1, 399.99, 399.99),
    (5, '2025-01-05', 'Headphones', 'Accessories', 4, 49.99, 199.96)
]

cur.executemany("INSERT OR IGNORE INTO sales VALUES (?, ?, ?, ?, ?, ?, ?);", sample_data)

# Commit changes and close connection
conn.commit()
conn.close()

print("Database and sales table created with sample data.")
