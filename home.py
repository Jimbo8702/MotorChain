import streamlit as st
import pandas as pd


#creates two containers
header = st.container()
body = st.container()

with header:
    st.title('MotorChain')

with header:
    st.markdown("""---""") 

with header:
    st.subheader('The premiere Blockchain car dealership!')

# creates all user input prompts
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
        max_chars=4,
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
        max_chars=17,
        key=None,
        autocomplete=None
    )
    st.text_input(
        label='Description of Vehicle',
        value='',
        max_chars=200,
        key=None,
        autocomplete=None
    )
    st.file_uploader(
        label='Input Vehicle Photo',
        type=['png', 'jpg'],
        accept_multiple_files=True,
        help='Input .jpg or .png of the vehicle you would like to list.'
    )

#Sidebar buttons (not yet functional)
    with header:
        st.sidebar.button(
            label='Connect Wallet',
            on_click=None
        )
    with body:
        st.sidebar.button(
            label='Marketplace',
            on_click=None
        )
        st.sidebar.button(
            label='Documentation',
            on_click=None
        )

    with body:
        if st.button('List Vehicle'):
            st.write('Listing!')
    
st.markdown("""---""") 

