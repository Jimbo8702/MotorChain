import yfinance as yf  # Yahoo finance to get stock data
import streamlit as st  # Streamlit to create the webapp 
import pandas as pd
from datetime import datetime
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

      
# ------ layout setting---------------------------
stock_selector = st.sidebar.container() 
stock_selector.markdown("## Auto Stocks")

# ---------Selectbox for users to pick a stock to evaluate-----------------

stock_picks = ("General Motors","Tesla","VW","Toyota","Honda","Ford","Stellantis","Hyundai","Volvo","Audi","BMW","Mercedes")  
ticker = stock_selector.selectbox("Pick a Stock",stock_picks)

# ---------Declare Ticker Symbols Based on User Selection-----------------

GM = 'GM'
Tesla = 'TSLA'  
Vwagon = 'VWAGY'
Toyota = 'TM'
Honda = 'HMC'
Ford = 'F'
Stellantis = 'STLA'
Hyundai = 'HYMTF'
Volvo = 'VLVLY'
Audi = 'AUDVF'
BMW = 'BMWYY'
Mercedes = 'DMLRY'

if ticker == "General Motors":
    ticker = GM 
if ticker == "Tesla":
    ticker = Tesla
if ticker == "VW":
    ticker = Vwagon
if ticker == "Toyota":
    ticker = Toyota
if ticker == "Honda":
    ticker = Honda
if ticker == "Ford":
    ticker = Ford
if ticker == "Stellantis":
    ticker = Stellantis
if ticker == "Hyundai":
    ticker = Hyundai
if ticker == "Volvo":
    ticker = Volvo
if ticker == "Audi":
    ticker = Audi
if ticker == "BMW":
    ticker = BMW
if ticker == "Mercedes":
    ticker = Mercedes


@st.cache(suppress_st_warning=True) 
def load_stock_data():
    stock_data = yf.Ticker(ticker).info
    return stock_data

data = load_stock_data() 

@st.cache(suppress_st_warning=True) 
def stock_history():
    stock_history = yf.Ticker(ticker).history(period="YTD" )
    return stock_history

history = stock_history()

@st.cache(suppress_st_warning=True) 
def load_stock_price():
    stock_price = yf.Ticker(ticker).info['regularMarketPrice']
    return stock_price

price = load_stock_price()
current_timestamp = datetime.now()
st.write(f"### {current_timestamp}")
st.write(f"## The price of {ticker} in USD is ${price:.2f}")
st.write("YTD Closing Price")
st.line_chart(history.Close,use_container_width=True)
if st.button("More Info"):
    st.write(data)

