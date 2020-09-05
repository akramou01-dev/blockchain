import hashlib
import json

def hash_string_256(string):
    return hashlib.sha256(string).hexdigest()

def hash_block(block):
    hashable_block = block.__dict__.copy()
    # on a ajouter copy() pour aussi faire an overite pour les liste de transactions dans le block car __dict__ converte juste le block en dict
    #we must convert all the tx in ordered_tx
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    return hash_string_256(json.dumps(hashable_block,sort_keys=True).encode()) 
    # sha256 is a method to hashing in 64 bits and return a hash in byts so we must call hexdegist
    