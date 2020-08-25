blockchain = []


def get_last_blockchain_value():
    """Returns the last value of the blockchain"""
    return blockchain[-1]


def add_value(value, last_transaction=[1]):
    """Append a new value as the last value of the blockchain"""
    blockchain.append([last_transaction, value])


def get_user_input():
    return float(input("enter your transaction amount :"))


add_value(get_user_input())
add_value(last_transaction=get_last_blockchain_value(),
          value=get_user_input())
add_value(get_user_input(), get_last_blockchain_value())
print(blockchain)
