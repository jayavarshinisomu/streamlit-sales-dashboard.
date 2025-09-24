import sqlite3
import pandas as pd

# Connect to SQLite sales database
conn = sqlite3.connect('sales.db')

# Query all data from sales table into a DataFrame
data = pd.read_sql_query("SELECT * FROM sales", conn)

# Display first 5 rows to check the data
print(data.head())

# Close the connection
conn.close()
