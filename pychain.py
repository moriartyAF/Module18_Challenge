# PyChain Ledger
################################################################################

# Imports
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib

# create a "Record" Data Class that consists of the following attributes: sender, receiver, and amount.
@dataclass
class Record:
    sender: str
    receiver: str
    amount: float = 0.0

# create a "Block" Data Class that consists of the following attributes: record, creator_id, prev_hash, timestamp, and nonce.
@dataclass
class Block:
    record: Record
    creator_id: int
    prev_hash: str = 0
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: str = 0

    # create a "hash_block" method 
    def hash_block(self):
        
        #define the sha256 hash function
        sha = hashlib.sha256()

        #encode and hash all 5 attributes
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

        #return hashes of all attributes        
        return sha.hexdigest()

# create a "PyChain" Data Class that consists of the following attributes: chain and difficulty.
@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4

    #add "proof_of_work" method
    def proof_of_work(self, block):
        calculated_hash = block.hash_block()
        num_of_zeros = "0" * self.difficulty

        #assess starting number of zeroes
        while not calculated_hash.startswith(num_of_zeros):
            block.nonce += 1
            calculated_hash = block.hash_block()

        #show winning hash & return the block
        print("Winning Hash", calculated_hash)
        return block

    
    #add "add_block" method
    def add_block(self, candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    #add "is_valid" method
    def is_valid(self):
        block_hash = self.chain[0].hash_block()

        #verify that the block hash is the same as the previous hash
        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Blockchain is invalid!")
                return False

            #set variable equal to hash block
            block_hash = block.hash_block()

        print("Blockchain is Valid")
        return True

#add streamlit cache decorator
@st.cache(allow_output_mutation=True)

#add "setup" method to return genesis block
def setup():
    print("Initializing Chain")
    return PyChain([Block("Genesis", 0)])

#add streamlit markdown text to display
st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

#set variable equal to setup method return value
pychain = setup()

#set user text entry variables for sender, receiver, and amount
sender_data = st.text_input("Sender")
receiver_data = st.text_input("Receiver")
amount_data = st.text_input("Amount")

#if user clicks "Add Block" button, go to last block in chain and previous hash value
if st.button("Add Block"):
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()

    #update new_block variables
    new_block = Block(
        record = Record(sender = sender_data,receiver = receiver_data,amount = amount_data),
        creator_id=42,
        prev_hash=prev_block_hash)

    #add new block to chain
    pychain.add_block(new_block)
    st.balloons()

#add streamlit markdown text to be displayed
st.markdown("## The PyChain Ledger")

##########   THE TEXT TO CREATE AND DISPLAY DATAFRAME OF CHAIN DATA HAS BEEN DISABLED DUE TO NON-FUNCTIONING METHODOLOGY, AS DISCUSSED IN CLASS ON OCT 20th  
#pychain_df = pd.DataFrame(pychain.chain)
#st.write(pychain_df)

#add slidebar to ise to adjust difficulty
difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)
pychain.difficulty = difficulty

#add text to slidebar showing instructions for use
st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", pychain.chain
)

#show details of selected block
st.sidebar.write(selected_block)

#if user clicks "Validate Chain" button, assess chain validaity and display result
if st.button("Validate Chain"):
    st.write(pychain.is_valid())

################################################################################
# Step 4:
# Test the PyChain Ledger by Storing Records

# Test your complete `PyChain` ledger and user interface by running your
# Streamlit application and storing some mined blocks in your `PyChain` ledger.
# Then test the blockchain validation process by using your `PyChain` ledger.
# To do so, complete the following steps:

# 1. In the terminal, navigate to the project folder where you've coded the
#  Challenge.

# 2. In the terminal, run the Streamlit application by
# using `streamlit run pychain.py`.

# 3. Enter values for the sender, receiver, and amount, and then click the "Add
# Block" button. Do this several times to store several blocks in the ledger.

# 4. Verify the block contents and hashes in the Streamlit drop-down menu.
# Take a screenshot of the Streamlit application page, which should detail a
# blockchain that consists of multiple blocks. Include the screenshot in the
# `README.md` file for your Challenge repository.

# 5. Test the blockchain validation process by using the web interface.
# Take a screenshot of the Streamlit application page, which should indicate
# the validity of the blockchain. Include the screenshot in the `README.md`
# file for your Challenge repository.
