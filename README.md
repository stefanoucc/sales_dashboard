# Machu Pouches Sales Dashboard

This repository contains a Streamlit application for visualizing sales data for Machu Pouches, a company that sells nicotine pouches. The dashboard connects to a Google Sheets document to pull real-time data and display key metrics and visualizations.

## Features

- **Sales Overview**: Total revenue, units sold, number of orders, average revenue per order, and average price per unit.
- **Interactive Sales Breakdown**: Revenue and units sold by product, seller, payment type, and sales channel. Visualized with interactive pie charts and bar charts using `plotly`.
- **Interactive Time-Series Analysis**: Visualize revenue, units sold, and orders over time with hover-over data points for exact values.
- **Top Buyers**: Lists the top 10 buyers by revenue and number of orders.
- **Interactive Filters**: Filter data by product, seller, payment type, sales channel, and date range.

## Setup and Installation

### Prerequisites

- Python 3.x
- A Google Sheets document named "Machu Pouches" with a worksheet named "Sales" published as a CSV.

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/stefanoucc/sales_dashboard.git
    cd sales_dashboard
    ```

2. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Streamlit app**:
    ```bash
    streamlit run app.py
    ```

### Usage

After running the app, open the provided local URL (usually `http://localhost:8501`) in your web browser. Use the sidebar to filter data by product, seller, payment type, sales channel, and date range.
