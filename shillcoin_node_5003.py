#Module 1 -Create a crypto currency

# To be install Flask
#Postman HTTP client

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask,jsonify,request
import requests
from uuid import uuid4
from urllib.parse import urlparse
# Part1 - Building a block chain

class Blockchain:
    def __init__(self):
        self.chain=[]
        self.transactions=[]
        self.nodes=set()
        self.create_block(proof=1,previous_hash='0')
    
    def create_block(self,proof,previous_hash):
        block= {'index': len(self.chain) + 1,
                'timestamp': str(datetime.datetime.now()),
                'proof':proof,
                'previous_hash':previous_hash,
                'transactions':self.transactions}
        
        self.transactions=[]
        self.chain.append(block)
        return block             
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self,previous_proof):
        new_proof=1
        check_proof=False
        while check_proof is False:
            hash_operation=hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]=='0000':
                check_proof=True
            else:
                new_proof+=1
        return new_proof
        
    def hash(self,block):
        encoded_block=json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block=chain[0]
        block_index=1
        while block_index<len(chain):
            if block['previous_hash']!= self.hash(previous_block):
                return False
            previous_proof=previous_block['proof']
            proof = block['proof']
            hash_operation=hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]!='0000':
                return False
            previous_block=block
            block_index+=1
            return True
   
    def add_transaction(self,sender,receiver,amount):
        self.transactions.append({
                'sender':sender,
                'receiver':receiver,
                'amount':amount})
        previous_block=self.get_previous_block()
        return previous_block['index'] + 1
        
    def add_node(self,address):
        parsed_url=urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    def replace_chain(self):
        network=self.nodes
        longest_chain=None
        max_length=len(self.chain)
        for node in network:
            response=response.get(f'http://{node}/get_chain')
            length=response.json()['length']
            chain=response.json()['chain']
            if length>max_length and self.is_chain_valid(chain):
                max_length=length
                longest_chain=chain
            if  longest_chain:
                self.chain=longest_chain
                return True
            return False
                
#Part 2 - Mining of block
    
# creating a web app
app = Flask(__name__)

# creating a block chain

blockchain=Blockchain()
# Mining the block



# creating a node address on port 5000
node_address = str(uuid4()).replace('-', '')

@app.route('/mine_block',methods=['GET'])

def mine_block():
    previous_block=block_chain.get_previous_block()
    previous_proof=block_chain.previous_block['proof']
    proof=block_chain.proof_of_work(previous_proof)
    previous_hash=block_chain.hash(previous_block)
    block=block_chain.create_block(proof,previous_hash)
    response={
            'message':'Congratulation , You just mined a block',
            'index':block['index'],
            'timestamp':block['timestamp'],
            'proof':block['proof'],
            'previous_hash':block['previous_hash'],
            'transactions':block['transactions']
            }
    return jsonify(response),200
    
        
# Getting the block chain        
@app.route('/get_chain',methods=['GET'])        
        
def get_chain():
    response={'chain':blockchain.chain,
              'length':len(blockchain.chain)
            }
    return jsonify(response),200
    
# 
@app.route('/get_chain',methods=['GET'])        

def is_valid():
    is_valid=blockchain.is_chain_valid(blockchain.chain)
    if is_valid():
        response={'message':'All good,The block chain is valid'}
    else:
        response={'message':'Shiller we have a problem,Block chain is not valid'}
    return jsonify(response),200

@app.route('/add_transaction',methods=['GET'])        

def add_transaction():
    json=reqeust.get_json()
    transaction_keys=['sender','receiver','amount']
    if not all (key in json for key in transaction_keys):
        return 'some elements of the transaction are missings',400
    index=blockchain.add_transaction(json['sender'],json['receiver'],json['amount'])
    response={'message':f'This transaction will be added to block {index}'}
    return jsonify(response),201

#connecting new node
@app.route('/connect_node',methods=['GET'])   

def connect_node():
    json=request.get_json()
    nodes=json.get('nodes')
    if nodes is None:
        return "no node",400
    for node in nodes:
        blockchain.add_node(node)
    response={'message':'All nodes are now connected,The shilcoin blockchain contains the following nodes:',
              'total_nodes':list(blockchain.nodes)}
    return jsonify(response),201
              
 
# resplace chain
@app.route('/replace_chain',methods=['GET'])  

def replace_chain():
    is_chain_replaced=blockchain.replace_chain()
    if is_chain_replaced():
        response={'message':'The node had different chain so the chain was replace by the longer chain:',
                  'new_chain':blockchain.chain}
    else:
        response={'message':' All good, The chain is the largest chain:',
                  'actual_chain':blockchain.chain}
    return jsonify(response),200
        


# run the app
    
app.run('0.0.0.0',port=5003)
        