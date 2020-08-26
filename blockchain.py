blockchain = []


def get_last_blockchain_value():
    """Returns the last value of the blockchain"""
    #chekking if the blockchian is empty or not 
    if len(blockchain) < 1 : 
        return None 
    return blockchain[-1]


def add_value(value, last_transaction):
    """Append a new value as the last value of the blockchain"""
    if last_transaction == None:
        blockchain.append(value)
    else : 
        blockchain.append([last_transaction, value])


def get_transaction_value():
    return float(input("enter your transaction amount :"))


def get_user_choice(): 
    return input("please enter your choice : ")

# add_value(last_transaction=get_last_blockchain_value(),
#           value=get_transaction_value())  


def print_blockchain_elements(): 
    i = 1
    for block in blockchain: 
        print("Printing Block N°=",i)
        print(block)
        i= i+1


while True: 
    print("please choose: ")
    print("1: Add new transaction value")
    print("2: Print the blockchain")
    print("q: Quit !")
    user_choice = get_user_choice()
    if user_choice == "1":

        if get_last_blockchain_value()== None:
            add_value(float(input("Enter the finrst element of the blockchain")),get_last_blockchain_value())
        else :
            add_value(get_transaction_value(),get_last_blockchain_value())
    elif user_choice =="q": 
        break
    elif user_choice =="2":
        print_blockchain_elements()
    else:
        print("Invalid input")


print("programme terminer")

