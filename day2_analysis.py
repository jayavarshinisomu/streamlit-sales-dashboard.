import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # Optional, for nicer charts

# Connect to the SQLite database and load data
conn = sqlite3.connect('sales.db')
data = pd.read_sql_query("SELECT * FROM sales", conn)
conn.close()

# ---- Day 4 Filtering and Analysis ----

# Filter data for a specific product
product_name = "Laptop"
filtered_data = data[data['Product'] == product_name]
print(f"Filtered Data for {product_name}:")
print(filtered_data)

# Convert 'Date' column to datetime if needed
data['Date'] = pd.to_datetime(data['Date'])

# Filter sales between two dates
start_date = '2025-01-01'
end_date = '2025-01-03'
date_filtered = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
print(f"Sales from {start_date} to {end_date}:")
print(date_filtered)

# Summary of filtered results
print("Total revenue for filtered data:", filtered_data['Revenue'].sum())
print("Total revenue for date range:", date_filtered['Revenue'].sum())

# ---- Basic Analysis ----

print(data.info())
print(data.head())
print(data.describe())

total_revenue = data['Revenue'].sum()
print(f"Total Revenue: {total_revenue}")

revenue_per_product = data.groupby('Product')['Revenue'].sum()
print("\nRevenue per Product:")
print(revenue_per_product)

revenue_per_category = data.groupby('Category')['Revenue'].sum()
print("\nRevenue per Category:")
print(revenue_per_category)

top_product = revenue_per_product.idxmax()
print(f"\nTop Product: {top_product}")

top_category = revenue_per_category.idxmax()
print(f"Top Category: {top_category}")

# ---- Visualizations ----

# Bar chart: Revenue per Product
plt.figure(figsize=(8,5))
revenue_per_product.plot(kind='bar', color='skyblue')
plt.title('Revenue per Product')
plt.xlabel('Product')
plt.ylabel('Revenue')
plt.tight_layout()
plt.show()

# Pie chart: Revenue per Category
plt.figure(figsize=(6,6))
revenue_per_category.plot(kind='pie', autopct='%1.1f%%')
plt.title('Revenue Distribution by Category')
plt.ylabel('')
plt.tight_layout()
plt.show()

# Line chart: Daily Revenue Trend
daily_revenue = data.groupby('Date')['Revenue'].sum()
plt.figure(figsize=(10,5))
daily_revenue.plot(kind='line', marker='o', color='green')
plt.title('Daily Revenue Trend')
plt.xlabel('Date')
plt.ylabel('Revenue')
plt.grid(True)
plt.tight_layout()
plt.show()
