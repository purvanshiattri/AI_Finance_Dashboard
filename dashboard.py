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
if isinstance(data.columns, pd.MultiIndex):
    data.columns = ['_'.join(col).strip() for col in data.columns.values]
else:
    # Normal case (single-level columns) — append symbol manually
    data.columns = [f"{col}_{stock_symbol}" for col in data.columns]
   

   

# Reset index to make 'Date' a column (instead of index)
data = data.reset_index()

# Show the table
st.subheader(f"{stock_symbol} Stock Data")
st.dataframe(data)

# Plot Closing Price
st.subheader(f"{stock_symbol} Closing Price Chart")
fig = px.line(data, x=f"Date", y=f"Close_{stock_symbol}", title=f"{stock_symbol} Closing Price Over Time")
st.plotly_chart(fig)

# Calculate moving averages
data[f"SMA_20_{stock_symbol}"] = data[f"Close_{stock_symbol}"].rolling(window=20).mean()
data[f"SMA_50_{stock_symbol}"] = data[f"Close_{stock_symbol}"].rolling(window=50).mean()

# Plot with moving averages
st.subheader(f"{stock_symbol} Closing Price with Moving Averages")
fig_ma = px.line(data, x="Date", y=[f"Close_{stock_symbol}", f"SMA_20_{stock_symbol}", f"SMA_50_{stock_symbol}"],
                 labels={"value": "Price", "variable": "Legend"},
                 title=f"{stock_symbol} - Closing Price with Moving Averages")
st.plotly_chart(fig_ma)


# --- KPI Summary Section ---
st.subheader(f"{stock_symbol} Key Performance Indicators (KPIs)")

# Get latest and previous data
latest_close = data[f"Close_{stock_symbol}"].iloc[-1]
prev_close = data[f"Close_{stock_symbol}"].iloc[-2] if len(data) > 1 else latest_close
price_change = latest_close - prev_close
pct_change = (price_change / prev_close) * 100 if prev_close != 0 else 0

high_price = data[f"High_{stock_symbol}"].max()
low_price = data[f"Low_{stock_symbol}"].min()
avg_volume = data[f"Volume_{stock_symbol}"].mean()

# Display KPIs in columns
col1, col2, col3, col4 = st.columns(4)
col1.metric("Current Price", f"${latest_close:.2f}")
col2.metric("Daily Change", f"{price_change:.2f}", f"{pct_change:.2f}%")
col3.metric("52-Week High", f"${high_price:.2f}")
col4.metric("Average Volume", f"{avg_volume:,.0f}")
