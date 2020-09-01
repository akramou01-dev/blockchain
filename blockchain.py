# Imports

from functools import reduce
import hashlib
import json
from collections import OrderedDict
import json
import pickle

# Exports

import hash_util


MINING_REWARDS = 10
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}
blockchain = []
blockchain.append(genesis_block)
open_transactions = []
owner = 'Akram'
participants = {'Akram'}

print(blockchain)


def get_last_blockchain_value():
    """Returns the last value of the blockchain"""
    # chekking if the blockchian is empty or not
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def save_data():
    with open('blockchain.p', mode="wb") as f:
        # for binary data we use the "wb" mode

        # f.write(json.dumps(blockchain))
        # f.write('\n')
        # f.write(json.dumps(open_transactions))
        save_data = {
            'chain': blockchain,
            'ot': open_transactions
        }
        f.write(pickle.dumps(save_data))


def load_data():
    # on a utiliser pickling ( using pickle ) pour garder le mm type de donnée mais on doit 
    # stocker les information en binaire mais on a paas besoin de overting the data we loaded from the file
    # les donnée resteront comme ils  sont
    # mais par contre le json nous donne les données en text alors il va supprimer qlq info 
    # et du coup on doit les faire overite
    # alors pour convertire les donnée on a le choix de travailler avec json et avec pickle
    with open('blockchain.p', mode='rb') as f:
        file_content =pickle.loads(f.read())
        global blockchain , open_transactions
        blockchain = file_content['chain']
        open_transactions = file_content['ot']
        # blockchain = json.loads(file_content[0][:-1])
        # # we want to overite the transactions of each block of the blockchain
        # blockchain = [{
        #     'previous_hash': block['previous_hash'],
        #      'index': block['index'],
        #      'proof': block['proof'],
        #      'transactions': [OrderedDict([
        #             ('sender',tx['sender']),
        #             ('recipient',tx['recipient']),
        #             ('amount',tx['amount'])
        #         ]
        #      ) for tx in block['transactions']],
        #     }
        #     for block in blockchain
        # ]
        # #  WE MUST USE THE SAME TYPE OF DATA (si on a travailler avec the ordereddict alors il faut continuer avec )
        # open_transactions = json.loads(file_content[1])
        # open_transactions = [OrderedDict([
        #             ('sender',tx['sender']),
        #             ('recipient',tx['recipient']),
        #             ('amount',tx['amount'])
        #         ]
        #      )  for tx in open_transactions]


load_data()


def valid_proof(transaction, last_hash, proof):
    guess = (str(transaction) + str(last_hash) + str(proof)).encode()
    print(guess)
    guess_hash = hash_util.hash_string_256(guess)
    print(guess_hash)
    # on peut spicifier n'import quelle condition
    return guess_hash[0:2] == "00"


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_util.hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def add_transaction(recipient, sender=owner, amount=1.0):
    """Append a new value as the last value of the blockchain"""

    transaction = OrderedDict(
        [('sender', sender), ('recipient', recipient), ('amount', amount)])
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(recipient)
        participants.add(sender)
        save_data()
        return True
    return False


def get_transaction_value():
    tx_recipient = input('Enter the recpient name of the transaction : ')
    tx_amount = float(input("enter your transaction amount :"))
    return (tx_recipient, tx_amount)


def get_user_choice():
    return input("please enter your choice : ")


# and the json.dumps is to convert the block into a string


def mine_block():
    """Creating the Blocks"""
    # we are using the Dictionaries data structure
    last_block = blockchain[-1]  # acces the last element of the blockchain
    # join sert a joindre des elements d'une liste et les separer par la caractére specefier avant
    hashed_block = hash_util.hash_block(last_block)
    proof = proof_of_work()
    reward_transaction = OrderedDict([
        ('sender', 'Mining'),
        ('recipient', owner),
        ('amount', MINING_REWARDS)
    ])
    print(reward_transaction)
    global open_transactions
    copied_open_transaction = open_transactions[:]
    copied_open_transaction.append(reward_transaction)

    block = {'previous_hash': hashed_block,
             'index': len(blockchain),
             'transactions': copied_open_transaction,
             'proof': proof,
             }
    blockchain.append(block)
    return True


def print_blockchain_elements():
    i = 1
    for i in range(len(blockchain)):
        print("Printing Block N°=", i)
        print(blockchain[i])
    else:
        print(" - " * 20)


def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_util.hash_block(blockchain[index-1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            return False

    return True


def verify_transaction(transaction):
    sender_balance = get_balence(transaction['sender'])
    return sender_balance >= transaction['amount']


def get_balence(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    # il faut aussi enclure les donnée qui ne sont pas encole mined genre dans les open transactions
    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amnt:  tx_sum + sum(tx_amnt)
                         if len(tx_amnt) > 0 else tx_sum + 0, tx_sender, 0)
    # amount_sent = 0
    # for tx in tx_sender:
    #     if len(tx) > 0:
    #         amount_sent += tx[0]

    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]

    #  WE USE THE REDUCE METHOD INSTEAD THE FOR LOOP
    amount_recived = reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount)
                            if len(tx_amount) > 0 else tx_sum + 0, tx_recipient, 0)
    # for tx in tx_recipient:
    #     if len(tx) > 0:
    #         amount_recived += tx[0]

    return amount_recived - amount_sent


wating_for_input = True
while wating_for_input:
    print("please choose: ")
    print("1: Add new transaction value")
    print("2: Mine a new block")
    print("3: Print the blockchain")
    print("4: Output Participants")
    print("h: Manipulate the blockchain")
    print("q: Quit !")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        print(recipient, amount)
        if add_transaction(recipient, amount=amount):
            print("Transaction added")
        else:
            print("Adding transation failed")
        print(open_transactions)
    elif user_choice == "q":
        wating_for_input = False
    elif user_choice == "2":
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == "3":
        print_blockchain_elements()
    elif user_choice == "4":
        print(participants)
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': {'sender': 'Chris', 'recipient': 'Max', 'amount': 4}
            }
    else:
        print("Invalid input")
    if not verify_chain():
        print("invalid blockchain")
        break
    print(" the balance of {} is : {:6.2f}".format(
        "Akram", get_balence("Akram")))
else:
    print("User left !")


print("programme terminer")
