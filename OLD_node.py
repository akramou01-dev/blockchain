
from blockchain import Blockchain
from uuid import uuid4
from utility.verification import Verification
from wallet import Wallet


class Node:
    def __init__(self):
        # self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        # initializing the blockchian 
        self.blockchain = Blockchain(self.wallet.public_key)

    def get_user_choice(self):
        return input("please enter your choice : ")

    def get_transaction_value(self):
        tx_recipient = input('Enter the recpient name of the transaction : ')
        tx_amount = float(input("enter your transaction amount :"))
        return (tx_recipient, tx_amount)

    def print_blockchain_elements(self):
        i = 1
        for i in range(len(self.blockchain.chain)):
            print("Printing Block N°=", i)
            print(self.blockchain.chain[i])
        else:
            print(" - " * 20)

    

    def listen_for_input(self):
        wating_for_input = True
        while wating_for_input:
            print("please choose: ")
            print("1: Add new transaction value")
            print("2: Mine a new block")
            print("3: Print the blockchain")
            print("4: check transaction va lidity")
            print("5: create wallet")
            print("6: load wallet")
            print("7: save keys")
            print("q: Quit !")
            user_choice = self.get_user_choice()
            if user_choice == "1":
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                signature= self.wallet.sign_transaction(self.wallet.public_key,recipient,amount)
                if self.blockchain.add_transaction(recipient, self.wallet.public_key,signature , amount=amount):
                    print("Transaction added")
                else:
                    print("Adding transation failed")
                print(self.blockchain.get_open_transactions())
            elif user_choice == "q":
                wating_for_input = False
            elif user_choice == "2":
                if not self.blockchain.mine_block():
                    print("Mining field, Wallet is inavailable!")
            elif user_choice == "3":
                self.print_blockchain_elements()
            elif user_choice == "4":
                if Verification.verify_transactions(self.blockchain.open_transactions, self.blockchain.get_balence):
                    print('All Transactions are valid')
                else:
                    print("There are invalid transaction")
            elif user_choice =="5":
                # saving the keys in files
                self.wallet.create_keys()
                # initializing the blockchian 
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice =="6":
                  self.wallet.load_keys()
            elif user_choice =="7":
              self.wallet.save_to_file()
            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print("invalid blockchain")
                break
            print(" the balance of {}  is : {:6.2f}".format(
                self.wallet.public_key, self.blockchain.get_balence()))
        else:
            print("User left !")
        print('Programme terminer !')

# on va verifier le contexte de l'execution si c le fichier principale ou bien un fichier importer 
if __name__ == '__main__':
    node = Node()
    node.listen_for_input()
