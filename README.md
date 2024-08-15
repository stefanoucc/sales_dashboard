# sales_dashboard
Sales Dashboard for machu pouches
# Machu Pouches Sales Dashboard

This repository contains a Streamlit application for visualizing sales data for Machu Pouches, a company that sells nicotine pouches. The dashboard connects to a Google Sheets document to pull real-time data and display key metrics and visualizations.

## Features

- **Sales Overview**: Total revenue, units sold, number of orders, average revenue per order, and average price per unit.
- **Sales Breakdown**: Revenue and units sold by product, seller, payment type, and sales channel.
- **Time-Series Analysis**: Visualize revenue, units sold, and orders over time.
- **Top Buyers**: Lists the top 10 buyers by revenue and number of orders.
- **Interactive Filters**: Filter data by product, seller, payment type, sales channel, and date range.

## Setup and Installation

### Prerequisites

- Python 3.x
- A Google Cloud service account with access to the Google Sheets API
- A Google Sheets document named "Machu Pouches" with a worksheet named "Sales"

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

3. **Set up Google Sheets API credentials**:
   - Obtain a service account JSON key file from your Google Cloud project.
   - Rename the file to `google_creds.json` and place it in the root of the repository.

4. **Run the Streamlit app**:
    ```bash
    streamlit run app.py
    ```

### Usage

After running the app, open the provided local URL (usually `http://localhost:8501`) in your web browser. Use the sidebar to filter data by product, seller, payment type, sales channel, and date range.

### Contact

If you have any questions or need further assistance, please contact Stefano Uccelli at stefanou24@gmail.com

