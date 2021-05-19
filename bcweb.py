# bcweb.py - blockchain with webapp interface 

import datetime # for timestamp 
import hashlib 
# Calculating the hash; In order to add digital; fingerprinting
import json # to store data in our blockchain 
from flask import Flask, jsonify

class Blockchain:
    # this block creates the first block and sets its Hash to 0
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        # this function is created to add further blocks into the chain
        block = {'index': len(self.chain) +1,
                'timestamp': str(datetime.datetime.now()),
                'proof': proof,
                'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    def print_previous_block(self):
        #this function displays the previous block
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        # this function for proof of work and used to successfully mine blocks
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '00000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
        
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()).hexdigest()

            if hash_operation[:4] != '00000':
                return False
            previous_block = block
            block_index += 1

        return True

# Creating the Web App usisng flask
app = Flask(__name__)

# Create the object of the class blockchain
blockchain = Blockchain()

# mining a new block 
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)

    response = {'message': 'A block is MINED',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}

    return jsonify(response), 200

# Display blockchain in json format
@app.route('/get_chain', methods=['GET'])
def display_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Check validity of blockchain
@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.chain_valid(blockchain.chain)

    if valid:
        response = {'message': 'Cha Bra, iz good'}
    else:
        response = {'message': 'Hmm, shits wierd bro'}
    return jsonify(response), 200

# run a local server 
app.run(host='127.0.0.1', port=7000)