import hashlib
import json

def hash_string_256(string):
    return hashlib.sha256(string).hexdigest()

def hash_block(block):
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict for tx in hashable_block['transactions']]
    print(hashable_block)
    return hash_string_256(json.dumps(hashable_block,sort_keys=True).encode()) 
    # sha256 is a method to hashing in 64 bits and return a hash in byts so we must call hexdegist
    