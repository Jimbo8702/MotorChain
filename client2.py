from io import StringIO
import streamlit as st
import pandas as pd
import nft_storage
from nft_storage.api import nft_storage_api
import json
from urllib3 import encode_multipart_formdata

df = pd.DataFrame()

header = st.container()
body = st.container()

with header:
    st.title("NFT Car Marketplace")

with body:
    owner_name = st.text_input(
        label="Owner Name", value="", max_chars=50, key=None, autocomplete=None
    )
    attribute = st.multiselect(
        label="Car Make", options=["Dodge", "Ford", "Tesla", "Chrysler", "Kia"]
    )
    if attribute == "Ford":
        st.multiselect(
            label="Model", options=["F150", "Focus", "Fusion"]
        )  # Need to loop through previous multiselect make to derive model & Type
    year = st.text_input(
        label="Year", value="", max_chars=50, key=None, autocomplete=None
    )
    # st.multiselect(
    #   label='Type',
    #  options=['Scatpack', 'Demon', 'RedEye', 'GT', 'AWD GT']
    # )
    vin = st.text_input(
        label="VIN Number", value="", max_chars=50, key=None, autocomplete=None
    )
    # image = st.file_uploader("Choose a file", type="jpeg")
    description = st.text_input(
        label="Description of Vehicle",
        value="",
        max_chars=50,
        key=None,
        autocomplete=None,
    )
    st.button(
        label="Submit",
    )

    with header:
        st.sidebar.button(label="Connect Wallet", on_click=None)
