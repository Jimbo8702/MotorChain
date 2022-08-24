from bip44 import Wallet
from web3 import Web3
from eth_account import Account
import json
import os
from typing import Dict, Any

import random

def load_json(path_to_json: str) -> Dict[str, Any]:
    """
    Purpose:
        Load json files
    Args:
        path_to_json (String): Path to  json file
    Returns:
        Conf: JSON file if loaded, else None
    """
    try:
        with open(path_to_json, "r") as config_file:
            conf = json.load(config_file)
            # print(conf)
            return conf

    except Exception as error:
        print(error)
        raise TypeError("Invalid JSON file")


def set_up_blockchain(contract:str, abi_path:str, priv, pub, vin):
     ############ Ethereum Setup ############
    
    
    PUBLIC_KEY = pub
    PRIVATE_KEY = priv
    INFURA_KEY = os.environ["INFURA_KEY"]

    network = os.environ["NETWORK"]
    ABI = None
    CODE_NFT = None
    CHAIN_ID = None
    w3 = None

    scan_url = ""

    eth_json = {}

    if network == "rinkeby":
        RINK_API_URL = f"https://rinkeby.infura.io/v3/{INFURA_KEY}"

        w3 = Web3(Web3.HTTPProvider(RINK_API_URL))
        ABI = load_json(abi_path)["abi"]  # get the ABI
        CODE_NFT = w3.eth.contract(address=contract, abi=ABI)  # The contract
        CHAIN_ID = 4

        
        scan_url = "https://rinkeby.etherscan.io/tx/"

    print(f"checking if connected to infura...{w3.isConnected()}")

    eth_json["w3"] = w3
    eth_json["contract"] = CODE_NFT
    eth_json["chain_id"] = CHAIN_ID
    eth_json["scan_url"] = scan_url
    eth_json["public_key"] = PUBLIC_KEY
    eth_json["private_key"] = PRIVATE_KEY
    eth_json["vin_number"] = vin


    return eth_json

def web3_mint(userAddress: str, tokenURI: str, eth_json: Dict[str, Any]) -> str:
    """
    Purpose:
        mint a token for user on blockchain
    Args:
        userAddress - the user to mint for
        tokenURI - metadat info for NFT
        eth_json - blockchain info
    Returns:
        hash - txn of mint
        tokenid - token minted
    """

    PUBLIC_KEY = eth_json["public_key"]
    CHAIN_ID = eth_json["chain_id"]
    w3 = eth_json["w3"]
    CODE_NFT = eth_json["contract"]
    PRIVATE_KEY = eth_json["private_key"]
    vin = eth_json['vin_number']

    # nonce = w3.eth.get_transaction_count(PUBLIC_KEY)
    nonce = random.randint(8, 150)

    # Create the contracrt
    mint_txn = CODE_NFT.functions.mint(userAddress, tokenURI, vin).buildTransaction(
        {
            "chainId": CHAIN_ID,
            "gas": 1000000,
            "gasPrice": w3.toWei("12", "gwei"),
            "nonce": nonce,
        }
    )

    signed_txn = w3.eth.account.sign_transaction(mint_txn, private_key=PRIVATE_KEY)

    w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    hash = w3.toHex(w3.keccak(signed_txn.rawTransaction))

    print(f"mint txn hash: {hash} ")

    receipt = w3.eth.wait_for_transaction_receipt(hash)  # hmmm have to wait...

    hex_tokenid = receipt["logs"][0]["topics"][3].hex()  # this is token id in hex

    # convert from hex to decmial
    tokenid = int(hex_tokenid, 16)
    print(f"Got tokenid: {tokenid}")

    return hash, tokenid

def main(vin, uri, mnemonic):
    # wallet
    wallet = Wallet(mnemonic)
    private, public = wallet.derive_account("eth", account=0 )
    account = Account.privateKeyToAccount(private)
    to_address = account.address
    priv_key = account.privateKey
    public_key = account.key
    print(to_address)
    # PRIVATE_KEY = Web3.toBytes(hexstr=priv_key.hex())
    # PUBLIC_KEY = Web3.toBytes(hexstr=public_key.hex())


    # contract
    contract_abi_path = "abi/abi.json"
    contract_address = "0x5370F4e7e71807CeF1E1A168ACbEBbE2Fd878587"
    token_uri = uri

    # run mint
    eth_json = set_up_blockchain(contract_address, contract_abi_path, priv=private, pub=public, vin=vin)
    txn_hash, tokenid = web3_mint(to_address, token_uri, eth_json)

    return print(f"txn_hash:{txn_hash} tokenid: {tokenid}")
    
  