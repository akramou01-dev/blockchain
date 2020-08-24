blockchain = ["test"]

def add_value(value): 
    blockchain.append([blockchain[-1],value])
    print(blockchain)

add_value(3)
add_value(2)
add_value(103)