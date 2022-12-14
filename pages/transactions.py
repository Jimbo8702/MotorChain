from termios import VINTR
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib
from ipfs_helper import load_json, upload_data

st.markdown("# Transactions")
st.sidebar.markdown("# Transactions")

header = st.container()
documentation = st.container()


@dataclass
class Car:
    owner: str
    make: str
    year: str
    model: str
    vin: str
    description: str
    image: str
    data_uri: str


@dataclass
class Record:
    sender: str
    receiver: str
    car: Car


@dataclass
class Block:
    record: Record
    creator_id: int
    prev_hash: str = "0"
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0

    def hash_block(self):
        sha = hashlib.sha256()

        record = str(self.record).encode()
        sha.update(record)

        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        nonce = str(self.nonce).encode()
        sha.update(nonce)

        return sha.hexdigest()


@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4

    def proof_of_work(self, block):

        calculated_hash = block.hash_block()

        num_of_zeros = "0" * self.difficulty

        while not calculated_hash.startswith(num_of_zeros):

            block.nonce += 1

            calculated_hash = block.hash_block()

        print("Wining Hash", calculated_hash)
        return block

    def add_block(self, candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    def is_valid(self):
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Blockchain is invalid!")
                return False

            block_hash = block.hash_block()

        print("Blockchain is Valid")
        return True


@st.cache(allow_output_mutation=True)
def setup():
    print("Initializing Chain")
    return PyChain([Block("Genesis", 0)])


motorchain = setup()

sender = st.text_input(label="sender", max_chars=100, autocomplete=None)
receiver = st.text_input(label="receiver", max_chars=100, autocomplete=None)
name = st.text_input(label="Name of car", max_chars=100, autocomplete=None)

if st.button("Add Block"):
    prev_block = motorchain.chain[-1]
    prev_block_hash = prev_block.hash_block()
    ipfs_hash = upload_data(name)
    ipfs_uri = "ipfs://{ipfs_hash}"
    car_info = load_json(f"./cars/{name}.json")
    user_car = Car(
        owner=car_info["name"],
        make=car_info["make"],
        year=car_info["year"],
        model=car_info["model"],
        vin=car_info["vin"],
        description=car_info["description"],
        image=car_info["image"],
        data_uri=ipfs_uri,
    )

    new_block = Block(
        creator_id=42,
        prev_hash=prev_block_hash,
        record=Record(sender, receiver, car=user_car),
    )

    motorchain.add_block(new_block)
    new_block = Block(
        creator_id=42,
        prev_hash=prev_block_hash,
        record=Record(sender, receiver, car=user_car),
    )

    motorchain.add_block(new_block)
    st.balloons()

motorchain_df = pd.DataFrame(motorchain.chain).astype(str)
st.write(motorchain_df)
