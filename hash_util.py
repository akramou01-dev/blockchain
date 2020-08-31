import hashlib
import json

def hash_string_256(string):
    return hashlib.sha256(string).hexdigest()

def hash_block(block):
    return hash_string_256(json.dumps(block,sort_keys=True).encode())
    # sha256 is a method to hashing in 64 bits and return a hash in byts so we must call hexdegist
    