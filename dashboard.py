import yfinance as yf
import pandas as pd
import plotly.express as px
import streamlit as st

# Sidebar inputs
stock_symbol = st.sidebar.text_input("Enter Stock Symbol", "AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-12-31"))

# Download stock data
data = yf.download(stock_symbol, start=start_date, end=end_date)

# Flatten MultiIndex columns if present
# --- FIX APPLIED HERE: Simplified Column Renaming ---
# Rename the columns to include the stock symbol (e.g., 'Close_AAPL') 
# This is cleaner and avoids the complex MultiIndex flattening logic which 
# was likely creating the extraneous data display.

new_columns = {col: f"{col}_{stock_symbol}" for col in data.columns}
data = data.rename(columns=new_columns)



# Reset index to make 'Date' a column (instead of index)
data = data.reset_index()

# Show the table
st.subheader(f"{stock_symbol} Stock Data")
st.dataframe(data)

# Plot Closing Price
st.subheader(f"{stock_symbol} Closing Price Chart")
fig = px.line(data, x="Date", y=f"Close_{stock_symbol}", title=f"{stock_symbol} Closing Price Over Time")
st.plotly_chart(fig)
