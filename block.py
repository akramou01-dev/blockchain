from time import time
from printable import Printable
class Block(Printable): 
    def __init__(self,index,previous_hash,transactions,proof,timestamp=None):
        self.index = index 
        self.previous_hash = previous_hash
        self.timestamp = time() if timestamp is None else timestamp 
        self.proof = proof 
        self.transactions = transactions 

    def __repr__(self):
        return """the index is {} and the previous hash is {} and the proof is {}. The Transactions are {} """.format(self.index,self.previous_hash,self.proof,self.transactions)
 