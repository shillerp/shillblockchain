#Module 1 -Create a block chain

# To be install Flask
#Postman HTTP client

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask,jsonify
# Part1 - Building a block chain

class Blockchain:
    def __init__(self):
        self.chain=[]
        self.create_block(proof=1,previous_hash='0')
    
    def create_block(self,proof,previous_hash):
        block= {'index': len(self.chain) + 1,
                'timestamp': str(datetime.datetime.now()),
                'proof':proof,
                'previous_hash':previous_hash}
                
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

#Part 2 - Mining of block
    
# creating a web app
app = Flask(__name__)

# creating a block chain

blockchain=Blockchain()
# Mining the block
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
            'previous_hash':block['previous_hash']
            }
    return jsonify(response),200
    
        
# Getting the block chain        
@app.route('/mine_block',methods=['GET'])        
        
def get_chain():
    response={'chain':blockchain.chain,
              'length':len(blockchain.chain)
            }
# run the app
    
app.run('0.0.0.0',port=5000)
        