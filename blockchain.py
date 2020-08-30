MINING_REWARDS = 10

genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
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


def add_transaction(recipient, sender=owner, amount=1.0):
    """Append a new value as the last value of the blockchain"""

    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
        }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(recipient)
        participants.add(sender)
        return True
    return False 


def get_transaction_value():
    tx_recipient = input('Enter the recpient name of the transaction : ')
    tx_amount = float(input("enter your transaction amount :"))
    return (tx_recipient, tx_amount)


def get_user_choice():
    return input("please enter your choice : ")


def hash_block(block):
    return '-'.join(str(block[key]) for key in block)


def mine_block():
    """Creating the Blocks"""
    # we are using the Dictionaries data structure
    last_block = blockchain[-1]  # acces the last element of the blockchain
    # join sert a joindre des elements d'une liste et les separer par la caractére specefier avant
    hashed_block = hash_block(last_block)
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARDS
    } 
    copied_open_transaction = open_transactions[:]
    copied_open_transaction.append(reward_transaction)
    block = {'previous_hash': hashed_block,
             'index': len(blockchain),
             'transactions': copied_open_transaction}
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
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False
    return True


def verify_transaction(transaction):
    sender_balance = get_balence(transaction['sender'])
    return sender_balance >= transaction['amount']


def get_balence(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    # il faut aussi enclure les donnée qui ne sont pas encole mined genre dans les open transactions
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]

    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]
    amount_recived = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_recived += tx[0]

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
    balance = get_balence('Akram')
    print("the balance is  :" + str(balance))
else:
    print("User left !")


print("programme terminer")
