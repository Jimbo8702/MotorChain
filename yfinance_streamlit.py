from time import strftime
import yfinance as yf  # Yahoo finance to get stock data
import streamlit as st  # Streamlit to create the webapp 
import pandas as pd
from datetime import datetime

st.title("MotorChain Auto Stock Portal")      
 
st.sidebar.header("Filter")

now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
time = now.strftime("%H:%M:%S")
date = now.strftime("%m/%d/%Y")
time = now.strftime("%H:%M:%S")

stock_picks = pd.read_csv("auto_companies.csv")



with st.form("form_1"):
    
    with st.sidebar:
        start_date = st.date_input("Start date", datetime(2022, 1, 1)) # User selects start date
        end_date = st.date_input("End date") # User selects end date, Default is Today
        ticker = st.selectbox("",stock_picks) # User picks a stock from the selectbox
        submitted = st.form_submit_button("Submit") # User clicks "run" to process the above selections 

         
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
def load_stock_price():
    stock_price = yf.Ticker(ticker).info['regularMarketPrice']
    return stock_price

price = load_stock_price()

@st.cache(suppress_st_warning=True) 
def load_stock_summary():
    stock_summary = yf.Ticker(ticker).info['longBusinessSummary']
    return stock_summary

stock_summary = load_stock_summary() 

@st.cache(suppress_st_warning=True) 
def stock_history():
    stock_history = yf.Ticker(ticker).history(period='1d', start=start_date, end=end_date )
    return stock_history

history = stock_history()

@st.cache(suppress_st_warning=True) 
def get_data_choices():
    stock_data = yf.Ticker(ticker).info
    return stock_data


stock_info = get_data_choices()
data_selection = st.sidebar.selectbox("",stock_info)


@st.cache(suppress_st_warning=True) 
def pull_data_choice():
    data_select = yf.Ticker(ticker).info[data_selection]
    st.sidebar.write(data_select)
    st.write(f"{date} \n {time}")
    st.write(f"## The price of {ticker} in USD is ${price:.2f}")
    st.line_chart(history.Close,use_container_width=True)
    st.line_chart(history.Volume,use_container_width=True)
    st.info(stock_summary)
    return data_select

pull = pull_data_choice()


    
    
    

    
    

    



    
    



        

    





