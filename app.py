import streamlit as st
import pandas as pd
import plotly.express as px

# Use the Google Sheets link with ?output=csv to get the data as a CSV
sheet_url = "https://docs.google.com/spreadsheets/d/1W_jm2sIkZiwrjHXL279VD_3nu2FyK6CUPtVyQepDQfo/export?format=csv"

# Read the Google Sheets data into a pandas DataFrame
df = pd.read_csv(sheet_url)

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y", errors='coerce')

# Clean and convert 'Payment Amount' to numeric by removing any non-numeric characters
df['Payment Amount'] = df['Payment Amount'].replace('[^\d.]', '', regex=True)
df['Payment Amount'] = df['Payment Amount'].str.replace(r'^\.', '', regex=True)
df['Payment Amount'] = pd.to_numeric(df['Payment Amount'], errors='coerce')

# Convert 'Amount' to numeric
df['Amount'] = df['Amount'].astype(int)
df['Amount'].value_counts(dropna=False)
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
st.title("MP Sales Dashboard")

# Overview Section
st.header("Sales Overview")
st.metric("Total Revenue", f"S/.{total_revenue:,.2f}")
st.metric("Total Units Sold", total_units_sold)
st.metric("Total Orders", total_orders)
st.metric("Average Revenue per Order", f"S/.{average_revenue_per_order:,.2f}")
st.metric("Average Price per Unit", f"S/.{average_price_per_unit:,.2f}")

# Sales Breakdown Section
st.header("Sales Breakdown")

# Pie chart for Revenue by Product
st.subheader("Revenue by Product")
fig = px.pie(filtered_df, values=revenue_by_product.values, names=revenue_by_product.index, title='Revenue by Product')
st.plotly_chart(fig)

# Pie chart for Units Sold by Product
st.subheader("Units Sold by Product")
fig = px.pie(filtered_df, values=units_sold_by_product.values, names=units_sold_by_product.index, title='Units Sold by Product')
st.plotly_chart(fig)

# Bar chart for Revenue by Seller
st.subheader("Revenue by Seller")
fig = px.bar(revenue_by_seller, x=revenue_by_seller.index, y=revenue_by_seller.values, 
             title='Revenue by Seller', color=revenue_by_seller.index, color_discrete_sequence=px.colors.qualitative.Plotly)
st.plotly_chart(fig)

# Bar chart for Units Sold by Seller
st.subheader("Units Sold by Seller")
fig = px.bar(units_sold_by_seller, x=units_sold_by_seller.index, y=units_sold_by_seller.values, 
             title='Units Sold by Seller', color=units_sold_by_seller.index, color_discrete_sequence=px.colors.qualitative.Plotly)
st.plotly_chart(fig)

# Bar chart for Revenue by Payment Type
st.subheader("Revenue by Payment Type")
fig = px.bar(revenue_by_payment_type, x=revenue_by_payment_type.index, y=revenue_by_payment_type.values, 
             title='Revenue by Payment Type', color=revenue_by_payment_type.index, color_discrete_sequence=px.colors.qualitative.Plotly)
st.plotly_chart(fig)

# Bar chart for Revenue by Sales Channel
st.subheader("Revenue by Sales Channel")
fig = px.bar(revenue_by_channel, x=revenue_by_channel.index, y=revenue_by_channel.values, 
             title='Revenue by Sales Channel', color=revenue_by_channel.index, color_discrete_sequence=px.colors.qualitative.Plotly)
st.plotly_chart(fig)

# Bar chart for Units Sold by Sales Channel
st.subheader("Units Sold by Sales Channel")
fig = px.bar(units_sold_by_channel, x=units_sold_by_channel.index, y=units_sold_by_channel.values, 
             title='Units Sold by Sales Channel', color=units_sold_by_channel.index, color_discrete_sequence=px.colors.qualitative.Plotly)
st.plotly_chart(fig)


# Time-Series Analysis Section
st.header("Time-Series Analysis")

# Revenue Over Time
st.subheader("Revenue Over Time")
fig = px.line(revenue_over_time, x=revenue_over_time.index.to_timestamp(), y=revenue_over_time.values, title='Revenue Over Time')
fig.update_xaxes(title_text='Date')
fig.update_yaxes(title_text='Revenue (S/.)')
st.plotly_chart(fig)

# Units Sold Over Time
st.subheader("Units Sold Over Time")
fig = px.line(units_sold_over_time, x=units_sold_over_time.index.to_timestamp(), y=units_sold_over_time.values, title='Units Sold Over Time')
fig.update_xaxes(title_text='Date')
fig.update_yaxes(title_text='Units Sold')
st.plotly_chart(fig)

# Orders Over Time
st.subheader("Orders Over Time")
fig = px.line(orders_over_time, x=orders_over_time.index.to_timestamp(), y=orders_over_time.values, title='Orders Over Time')
fig.update_xaxes(title_text='Date')
fig.update_yaxes(title_text='Number of Orders')
st.plotly_chart(fig)

# Top Buyers Section
st.header("Top Buyers")
st.subheader("Top 10 Buyers by Revenue")
st.table(top_buyers_by_revenue)
st.subheader("Top 10 Buyers by Number of Orders")
st.table(top_buyers_by_orders)
