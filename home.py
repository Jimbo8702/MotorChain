from unicodedata import name
import streamlit as st
import pandas as pd
from time import strftime
import yfinance as yf  # Yahoo finance to get stock data
from datetime import datetime
import webbrowser
from ipfs_helper import write_file


# creates two containers
header = st.container()
body = st.container()

with header:
    st.title("MotorChain")

with header:
    st.markdown("""---""")

with header:
    st.subheader("The premiere Blockchain car dealership!")


# creates all user input prompts
with body:
    # st.text_input(
    # label='ETH Wallet ID',
    # max_chars=42,
    # key=None,
    # autocomplete=None
    # )
    # st.text_input(label="Mnemonic Phrase", max_chars=512, key=None, autocomplete=None)
    owner_name = st.text_input(
        label="Owner Name", value="", max_chars=50, key=None, autocomplete=None
    )
    attribute = st.multiselect(
        label="Car Make",
        options=[
            "Dodge",
            "Ford",
            "Tesla",
            "Chrysler",
            "Kia",
            "Volkswagen",
            "Honda",
            "Chevrolet",
            "Mercedes",
            "Jeep",
            "Porsche",
            "Nissan",
        ],
    )
    year = st.text_input(
        label="Year", value="", max_chars=4, key=None, autocomplete=None
    )
    model = st.text_input(
        label="Type", value="", max_chars=25, key=None, autocomplete=None
    )
    vin = st.text_input(
        label="VIN Number", value="", max_chars=17, key=None, autocomplete=None
    )
    description = st.text_input(
        label="Description of Vehicle",
        value="",
        max_chars=200,
        key=None,
        autocomplete=None,
    )
    image = st.file_uploader(
        label="Input Vehicle Photo",
        # type=['png', 'jpeg'],
        type="jpeg",
        # accept_multiple_files=True,
        help="Input .jpeg of the vehicle you would like to list.",
    )
    # if st.button(label="Submit"):
    #     write_file(
    #         context={
    #             "name": owner_name,
    #             "make": attribute[0],
    #             "year": year,
    #             "model": model,
    #             "vin": vin,
    #             "description": description,
    #         },
    #         image=image,
    #     )


# Sidebar buttons (not yet functional)
st.sidebar.markdown("# Home")

with body:
    if st.button("List Vehicle"):
        st.write("Listing!")
        write_file(
            context={
                "name": owner_name,
                "make": attribute[0],
                "year": year,
                "model": model,
                "vin": vin,
                "description": description,
            },
            image=image,
        )


st.markdown("""---""")

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
        start_date = st.date_input(
            "Start date", datetime(2022, 1, 1)
        )  # User selects start date
        end_date = st.date_input("End date")  # User selects end date, Default is Today
        ticker = st.selectbox("", stock_picks)  # User picks a stock from the selectbox
        submitted = st.form_submit_button(
            "Submit"
        )  # User clicks "run" to process the above selections


GM = "GM"
Tesla = "TSLA"
Vwagon = "VWAGY"
Toyota = "TM"
Honda = "HMC"
Ford = "F"
Stellantis = "STLA"
Hyundai = "HYMTF"
Volvo = "VLVLY"
Audi = "AUDVF"
BMW = "BMWYY"
Mercedes = "DMLRY"

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
    stock_price = yf.Ticker(ticker).info["regularMarketPrice"]
    return stock_price


price = load_stock_price()


@st.cache(suppress_st_warning=True)
def load_stock_summary():
    stock_summary = yf.Ticker(ticker).info["longBusinessSummary"]
    return stock_summary


stock_summary = load_stock_summary()


@st.cache(suppress_st_warning=True)
def stock_history():
    stock_history = yf.Ticker(ticker).history(
        period="1d", start=start_date, end=end_date
    )
    return stock_history


history = stock_history()


@st.cache(suppress_st_warning=True)
def get_data_choices():
    stock_data = yf.Ticker(ticker).info
    return stock_data


stock_info = get_data_choices()


@st.cache(suppress_st_warning=True)
def pull_data_choice():
    st.write(f"{date} \n {time}")
    st.subheader(f"One share of {ticker} is ${price:.2f} today!")
    st.line_chart(history.Close, use_container_width=True)
    st.line_chart(history.Volume, use_container_width=True)
    st.info(stock_summary)
    data_selection = st.selectbox("", stock_info)
    data_select = yf.Ticker(ticker).info[data_selection]
    st.write(f"{data_select}")
    return data_select


pull = pull_data_choice()
