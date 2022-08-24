# take input => store in nft.storage => get uri => mint nft
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
# from bip44 import Wallet
# from web3 import Web3
# from eth_account import Account
import requests
import os
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from ipfs_helper import write_file
from web3_helper import main
# w3 = Web3(
#     Web3.HTTPProvider("https://rinkeby.infura.io/v3/7f3f1629b1e54d3d8b4c2696016b16db")
# )
# if w3.isConnected():
#     st.text("Connected to web3")


# pk = st.text_input("Wallet public key")
# mn = st.text_input("Mnemonic")

# if pk and mn:
#     wallet = Wallet(mn)
#     private, public = wallet.derive_account("eth")
#     account = Account.privateKeyToAccount(private)
st.text("Write file")
name = st.text_input("Name")
description = st.text_input("Vin")
model = st.text_input("Model")
image = st.file_uploader("Image", type="jpeg")
context = {"name": name, "description": description, "image": image}
uri = ""
if name and description and model and image:
    ipfs_hash = write_file(context, image=image)
    uri = f"ipfs://{ipfs_hash}"


mnemonic_seed = st.text_input("mnemonic phrase for your account") 
address = st.text_input("account address") 
if mnemonic_seed and address:
    main(uri, mnemonic_seed)


