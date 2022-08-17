import streamlit as st
import pandas as pd

df = pd.DataFrame()

header = st.container()
body = st.container()

with header:
    st.title('NFT Car Marketplace')

with body:
    st.text_input(
        label='Owner Name',
        value='',
        max_chars=50,
        key=None,
        autocomplete=None
    )
    attribute = st.multiselect(
        label='Car Make',
        options=['Dodge', 'Ford', 'Tesla', 'Chrysler', 'Kia']
    )
    if attribute == 'Ford':
        st.multiselect(
            label='Model',
            options=['F150', 'Focus', 'Fusion']
    ) # Need to loop through previous multiselect make to derive model & Type
    st.text_input(
        label='Year',
        value='',
        max_chars=50,
        key=None,
        autocomplete=None
    )
    #st.multiselect(
     #   label='Type',
      #  options=['Scatpack', 'Demon', 'RedEye', 'GT', 'AWD GT']
   # )
    st.text_input(
        label='VIN Number',
        value='',
        max_chars=50,
        key=None,
        autocomplete=None
    )
    st.text_input(
        label='Description of Vehicle',
        value='',
        max_chars=50,
        key=None,
        autocomplete=None

    )

    with header:
        st.sidebar.button(
            label='Connect Wallet',
            on_click=None
        )