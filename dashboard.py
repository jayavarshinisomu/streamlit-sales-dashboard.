import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Connect and load data
conn = sqlite3.connect('sales.db')
data = pd.read_sql_query("SELECT * FROM sales", conn)
conn.close()

# Convert Date for filtering
data['Date'] = pd.to_datetime(data['Date'])

st.title("Interactive Sales Dashboard")

# Sidebar filters
product_filter = st.sidebar.multiselect(
    "Select Product(s):",
    options=data['Product'].unique(),
    default=data['Product'].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Category(s):",
    options=data['Category'].unique(),
    default=data['Category'].unique()
)

date_filter = st.sidebar.date_input(
    "Select Date Range:",
    [data['Date'].min(), data['Date'].max()]
)

# Filter data based on user selections
filtered_data = data[
    (data['Product'].isin(product_filter)) &
    (data['Category'].isin(category_filter)) &
    (data['Date'] >= pd.to_datetime(date_filter[0])) &
    (data['Date'] <= pd.to_datetime(date_filter[1]))
]

st.write(f"Showing {len(filtered_data)} records after filtering:")
st.dataframe(filtered_data)

# Export filtered data as CSV
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv_data = convert_df_to_csv(filtered_data)

st.download_button(
    label="Download filtered data as CSV",
    data=csv_data,
    file_name='filtered_sales.csv',
    mime='text/csv',
)

# --- KPI Metrics ---

total_revenue = filtered_data['Revenue'].sum() if not filtered_data.empty else 0
total_quantity = filtered_data['Quantity'].sum() if not filtered_data.empty else 0
average_order_value = (total_revenue / len(filtered_data)) if len(filtered_data) > 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Quantity Sold", f"{total_quantity:,}")
col3.metric("Average Order Value", f"${average_order_value:,.2f}")

# --- Charts with empty data checks ---

# Bar chart: Revenue per Product
revenue_per_product = filtered_data.groupby('Product')['Revenue'].sum()
if revenue_per_product.shape[0] > 0:
    fig1, ax1 = plt.subplots()
    revenue_per_product.plot(kind='bar', ax=ax1, color='skyblue')
    ax1.set_title('Revenue per Product')
    ax1.set_xlabel('Product')
    ax1.set_ylabel('Revenue')
    st.pyplot(fig1)
else:
    st.warning("No data available for Revenue per Product chart with the selected filter.")

# Pie chart: Revenue per Category
revenue_per_category = filtered_data.groupby('Category')['Revenue'].sum()
if revenue_per_category.shape[0] > 0:
    fig2, ax2 = plt.subplots()
    revenue_per_category.plot(kind='pie', ax=ax2, autopct='%1.1f%%', startangle=90)
    ax2.set_ylabel('')
    ax2.set_title('Revenue Distribution by Category')
    st.pyplot(fig2)
else:
    st.warning("No data available for Revenue per Category chart with the selected filter.")

# Line chart: Daily Revenue Trend
daily_revenue = filtered_data.groupby('Date')['Revenue'].sum()
if daily_revenue.shape[0] > 0:
    fig3, ax3 = plt.subplots()
    daily_revenue.plot(kind='line', ax=ax3, marker='o', color='green')
    ax3.set_title('Daily Revenue Trend')
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Revenue')
    ax3.grid(True)
    st.pyplot(fig3)
else:
    st.warning("No data available for Daily Revenue Trend chart with the selected filter.")
