import streamlit as st
import pandas as pd

# Use the Google Sheets link with ?output=csv to get the data as a CSV
sheet_url = "https://docs.google.com/spreadsheets/d/1WLn7DH3F1Sm5ZSEHgWVEILWvvjFRsrE0b9xKrYU43Hw/export?format=csv"

# Read the Google Sheets data into a pandas DataFrame
df = pd.read_csv(sheet_url)

# Streamlit app
st.title("Machu Pouches Sales Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
product_filter = st.sidebar.multiselect("Select Product", df['Product'].unique())
seller_filter = st.sidebar.multiselect("Select Seller", df['Seller'].unique())
payment_type_filter = st.sidebar.multiselect("Select Payment Type", df['Payment Type'].unique())
channel_filter = st.sidebar.multiselect("Select Sales Channel", df['Channel'].unique())
date_filter = st.sidebar.date_input("Select Date Range", [df['Date'].min(), df['Date'].max()])

# Filter DataFrame based on sidebar inputs
filtered_df = df.copy()
if product_filter:
    filtered_df = filtered_df[filtered_df['Product'].isin(product_filter)]
if seller_filter:
    filtered_df = filtered_df[filtered_df['Seller'].isin(seller_filter)]
if payment_type_filter:
    filtered_df = filtered_df[filtered_df['Payment Type'].isin(payment_type_filter)]
if channel_filter:
    filtered_df = filtered_df[filtered_df['Channel'].isin(channel_filter)]
if date_filter:
    start_date, end_date = date_filter
    filtered_df = filtered_df[(filtered_df['Date'] >= pd.to_datetime(start_date)) & (filtered_df['Date'] <= pd.to_datetime(end_date))]

# Sales Overview
total_revenue = filtered_df['Payment Amount'].sum()
total_units_sold = filtered_df['Amount'].sum()
total_orders = filtered_df['Order ID'].nunique()
average_revenue_per_order = total_revenue / total_orders if total_orders > 0 else 0
average_price_per_unit = total_revenue / total_units_sold if total_units_sold > 0 else 0

# Sales Breakdown
revenue_by_product = filtered_df.groupby('Product')['Payment Amount'].sum()
units_sold_by_product = filtered_df.groupby('Product')['Amount'].sum()
revenue_by_seller = filtered_df.groupby('Seller')['Payment Amount'].sum()
units_sold_by_seller = filtered_df.groupby('Seller')['Amount'].sum()
revenue_by_payment_type = filtered_df.groupby('Payment Type')['Payment Amount'].sum()
revenue_by_channel = filtered_df.groupby('Channel')['Payment Amount'].sum()
units_sold_by_channel = filtered_df.groupby('Channel')['Amount'].sum()

# Top Buyers
top_buyers_by_revenue = filtered_df.groupby('Buyer')['Payment Amount'].sum().nlargest(10)
top_buyers_by_orders = filtered_df.groupby('Buyer')['Order ID'].nunique().nlargest(10)

# Time-Series Analysis
revenue_over_time = filtered_df.groupby(filtered_df['Date'].dt.to_period('D'))['Payment Amount'].sum()
units_sold_over_time = filtered_df.groupby(filtered_df['Date'].dt.to_period('D'))['Amount'].sum()
orders_over_time = filtered_df.groupby(filtered_df['Date'].dt.to_period('D'))['Order ID'].nunique()

# Streamlit Dashboard Layout
st.title("Machu Pouches Sales Dashboard")

# Overview Section
st.header("Sales Overview")
st.metric("Total Revenue", f"S/.{total_revenue:,.2f}")
st.metric("Total Units Sold", total_units_sold)
st.metric("Total Orders", total_orders)
st.metric("Average Revenue per Order", f"S/.{average_revenue_per_order:,.2f}")
st.metric("Average Price per Unit", f"S/.{average_price_per_unit:,.2f}")

# Sales Breakdown Section
st.header("Sales Breakdown")
st.subheader("Revenue by Product")
st.bar_chart(revenue_by_product)
st.subheader("Units Sold by Product")
st.bar_chart(units_sold_by_product)
st.subheader("Revenue by Seller")
st.bar_chart(revenue_by_seller)
st.subheader("Units Sold by Seller")
st.bar_chart(units_sold_by_seller)
st.subheader("Revenue by Payment Type")
st.bar_chart(revenue_by_payment_type)
st.subheader("Revenue by Sales Channel")
st.bar_chart(revenue_by_channel)
st.subheader("Units Sold by Sales Channel")
st.bar_chart(units_sold_by_channel)

# Time-Series Analysis Section
st.header("Time-Series Analysis")
st.line_chart(revenue_over_time)
st.line_chart(units_sold_over_time)
st.line_chart(orders_over_time)

# Top Buyers Section
st.header("Top Buyers")
st.subheader("Top 10 Buyers by Revenue")
st.table(top_buyers_by_revenue)
st.subheader("Top 10 Buyers by Number of Orders")
st.table(top_buyers_by_orders)
