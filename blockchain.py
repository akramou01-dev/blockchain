blockchain = []


def get_last_blockchain_value():
    """Returns the last value of the blockchain"""
    # chekking if the blockchian is empty or not
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_value(value, last_transaction):
    """Append a new value as the last value of the blockchain"""
    if last_transaction == None:
        blockchain.append([value])
    else:
        blockchain.append([last_transaction, value])


def get_transaction_value():
    return float(input("enter your transaction amount :"))


def get_user_choice():
    return input("please enter your choice : ")

# add_value(last_transaction=get_last_blockchain_value(),
#           value=get_transaction_value())


def print_blockchain_elements():
    i = 1
    for i in range(len(blockchain)):
        print("Printing Block N°=", i)
        print(blockchain[i])
    else : 
        print( " - " * 20)


def verify_chain():
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
        block_index+=1

    # for block in blockchain:
    #     if block_index==0:
    #         """ pour ignorer la premiere case car elle n'a pas de previous block"""
    #         block_index+=1
    #         continue
    #     elif block[0] == blockchain[block_index - 1]:
    #         is_valid = True
    #     else:
    #         is_valid = False
    #         break
    #     block_index+=1
    return is_valid 

wating_for_input = True
while wating_for_input:
    print("please choose: ")
    print("1: Add new transaction value")
    print("2: Print the blockchain")
    print("h: Manipulate the blockchain")
    print("q: Quit !")
    user_choice = get_user_choice()
    if user_choice == "1":
        if get_last_blockchain_value() == None:
            add_value(float(input(
                "Enter the first element of the blockchain : ")), get_last_blockchain_value())
        else:
            add_value(get_transaction_value(), get_last_blockchain_value())
    elif user_choice == "q":
        wating_for_input = False    
    elif user_choice == "2":
        print_blockchain_elements()
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    else:
        print("Invalid input")
    if not verify_chain():
        print("invalid blockchain")
        break
else : 
    print("User left !")


print("programme terminer")
