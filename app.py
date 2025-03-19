import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import requests
import main
# Kelas-kelas Anda tetap sama, saya hanya tambahkan bagian Streamlit di bawah ini

# API Key
api_key = 'SRWEWJNP9LO1RWR6'
TIME_SERIES_INTRADAY = 'TIME_SERIES_INTRADAY'
TIME_SERIES_DAILY = 'TIME_SERIES_DAILY'
TIME_SERIES_WEEKLY = 'TIME_SERIES_WEEKLY'
TIME_SERIES_WEEKLY_ADJUSTED = 'TIME_SERIES_WEEKLY_ADJUSTED'
TIME_SERIES_MONTHLY = 'TIME_SERIES_MONTHLY'
TIME_SERIES_MONTHLY_ADJUSTED = 'TIME_SERIES_MONTHLY_ADJUSTED'
# Inisialisasi class
stock = main.CoreStock(api_key)
options = main.OptionsData(api_key)

# Konfigurasi halaman
st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)

# Sidebar
st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Stock Ticker", "AAPL").upper()
timeframe = st.sidebar.selectbox(
    "Timeframe",
    ["Intraday", "Daily", "Weekly", "Monthly"]
)
interval = st.sidebar.selectbox(
    "Interval (for Intraday)",
    ["1min", "5min", "15min", "30min", "60min"]
)
size = st.sidebar.radio("Data Size", ["compact", "full"])

# Mapping timeframe ke function
timeframe_map = {
    "Intraday": TIME_SERIES_INTRADAY,
    "Daily": TIME_SERIES_DAILY,
    "Weekly": TIME_SERIES_WEEKLY,
    "Monthly": TIME_SERIES_MONTHLY
}

# Main content
st.title("📈 Stock Market Dashboard")
st.markdown(f"Showing data for **{ticker}**")

# Layout dengan columns
col1, col2 = st.columns(2)

# Function untuk membuat chart
def create_chart(df, title):
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)
    fig = px.line(
        df,
        y="4. close",
        title=title,
        labels={"4. close": "Price (USD)", "index": "Date"}
    )
    fig.update_layout(
        template="plotly_dark",
        height=400
    )
    return fig

# Stock Price Section
with col1:
    st.subheader("Stock Price History")
    try:
        df = stock.stock_df(
            ticker=ticker,
            function=timeframe_map[timeframe],
            interval=interval,
            size=size,
            debug=False
        )
        
        # Tampilkan chart
        fig = create_chart(df, f"{ticker} {timeframe} Price")
        st.plotly_chart(fig, use_container_width=True)
        
        # Tampilkan stats
        st.metric("Latest Price", f"${df['4. close'][0]:.2f}")
        
    except Exception as e:
        st.error(f"Error fetching stock data: {str(e)}")

# Options Section
with col2:
    st.subheader("Options Data")
    show_options = st.checkbox("Show Options Data")
    
    if show_options:
        try:
            options_date = st.date_input("Options Date", value=None)
            options_df = options.options(
                ticker=ticker,
                date=options_date.strftime("%Y-%m-%d") if options_date else None
            )
            
            # Format options data
            if not options_df.empty:
                options_df['expiration_date'] = pd.to_datetime(options_df['expiration_date'])
                st.dataframe(
                    options_df.style.format({
                        'strike': '${:.2f}',
                        'last_price': '${:.2f}',
                        'bid': '${:.2f}',
                        'ask': '${:.2f}'
                    }),
                    height=300
                )
            else:
                st.warning("No options data available")
                
        except Exception as e:
            st.error(f"Error fetching options data: {str(e)}")

# Global Market Status
with st.expander("Global Market Status"):
    try:
        market_df = stock.global_market()
        st.dataframe(
            market_df.style.highlight_max(subset=['current_status']),
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Error fetching market status: {str(e)}")

# Custom CSS untuk styling
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    .stMetric {
        background-color: #282c34;
        padding: 10px;
        border-radius: 5px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)