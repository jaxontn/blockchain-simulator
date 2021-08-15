#module 1 - create a Blockchain

#To be installed:
#Flask==0.12.2: pip install Flask==0.12.2
#Postman HTTP Client: https://www.getpostman.com/

#Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 - Building a Blockchain

class Blockchain:

    def __init__(self): #self will refer to the object that we create once the class is made
        self.chain = [] #an empty list

        #creating the genesis block (first block of the blockchain)
        self.create_block(proof = 1, previous_hash = '0')
    

    def create_block(self, proof, previous_hash):
        block = {'index' : len(self.chain) + 1,
                'timestamp' : str(datetime.datetime.now()),
                'proof' : proof,
                'previous_hash' : previous_hash}
        #we are gonna make a dictionary that will define each block in the blockchain with its four
        #essential keys (e.g. index, timestamp, proof, previous_hash)
        self.chain.append(block)
        return block


    def get_previous_block(self):
        return self.chain[-1]; #gets the left block of the chain


    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            #try, fail, increment new proof
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:3] == '0000': #to get the first 4 characters are == to '0000'
                                             #in that case the miner wins
                check_proof = True
            else:
                check_proof = False
                new_proof += 1
        return new_proof


    def hash(self, block): #we are going to hash a block of our blockchain
        encoded_block = json.dumps(block, sort_keys= True).encode()
        return hashlib.sha256(encoded_block).hexdigest()


    def is_chain_valid(self, chain):
        #we are going to check 2 things:
        #1. we're gonna check that the previous hash of each block is equal to the hash of its previous block 
        #2. proof of each block is valid according to our proof of work

        previous_block = chain[0]
        block_index = 1

        #we need to iterate on all the chains
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

# Part 2 - Mining our Blockchain

#Create a Web App 
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

#Create a Blockchain
blockchain = Blockchain()

#Mining a new block
#flask.pocoo.org/docs/0.12/quickstart
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    #previous_block = blockchain.get_previous_block()
    #previous_proof = previous_block['proof']
    #proof = blockchain.proof_of_work(previous_proof)
    #previous_hash = blockchain.hash(previous_block)
    #block = blockchain.create_block(proof, previous_hash)

    #we are creating a dictionary
    response = {'message' : 'Congratulations, you just mined a block!'}#,
                 #'index' : block['index'],
                 #'timestamp' : block['timestamp'],
                 #'proof' : block['proof'],
                 #'previous_hash' : block['previous_hash']}
    return jsonify(response), 200

#getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain' : blockchain.chain,
                 'length' : len(blockchain.chain)}
    return jsonify(response), 200
    
    
#Running the app
app.run(host = '0.0.0.0', port = 5000)          