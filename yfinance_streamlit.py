"""

Cryptocurency Daily Prices Webapp

- Using streamlit and Yahoo Finance


"""

from curses import use_default_colors
import yfinance as yf  # Yahoo finance to get stock data
import streamlit as st  # Streamlit to create the webapp
from PIL import Image  # Import Pillow to add icons
from urllib.request import urlopen  # To add URLS
import pandas as pd


# Define bitcoin and ethereum and other cryptocurrency abbreviation used by Yahoo Finance.
Bitcoin = 'BTC-USD'
GeneralMotors = 'GM'
Tesla = 'TSLA'
BTC_Data = yf.Ticker(Bitcoin)

GM_Data = yf.Ticker(GeneralMotors)
TSLA_Data = yf.Ticker(Tesla)


#for all_tickers.info[["industry"] == ["Auto Manufacturers"]]:

GM_History = GM_Data.history(period="max")
GM_Price = GM_Data.info['regularMarketPrice']

TSLA_History = TSLA_Data.history(period="max")
TSLA_Price = TSLA_Data.info['regularMarketPrice']

imageLINK = Image.open(urlopen('https://s2.coinmarketcap.com/static/img/coins/64x64/1975.png'))
st.image(imageLINK, use_column_width=False)

# GM Stock Price
st.write(""" ## General Motors Company  """, f"${GM_Price:.2f}")
image_GM = Image.open('./images/gm.png')
st.image(image_GM, use_column_width=False)
st.line_chart(GM_History.Close, use_container_width=True)

GM_sector = GM_Data.info['sector']
st.write(GM_sector)

# Tesla Stock Price
st.write(""" ## Tesla, Inc. """, f"${TSLA_Price:.2f}")
image_TSLA = Image.open('./images/tsla.png')
st.image(image_TSLA, use_column_width=False)
st.line_chart(TSLA_History.Close, use_container_width=True)

#TSLA_sector = TSLA_Data.info['sector']


