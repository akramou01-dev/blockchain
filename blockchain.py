# Imports

from functools import reduce
import hashlib
import json
from collections import OrderedDict
import json
import pickle
from block import Block
from transaction import Transaction
from utility.verification import Verification
from wallet import Wallet

# Exports

from utility import hash_util

MINING_REWARDS = 10

print(__name__)
class Blockchain():
    def __init__(self, hosting_node_id):
        # Initializing the empty blockchain
        genesis_block = Block(0, '', [], 100, 0)
        # on peut declarer chain et open_transactions comme des attribute privé
        self.chain = [genesis_block]
        # for the inhandle transactions
        self.open_transactions = []
        self.load_data()

        self.hosting_node = hosting_node_id

    # Getters
    @property
    def chain(self):
        return self.__chain[:]
    #Setters
    @chain.setter
    def chain(self,value):
        self.__chain = value
    

    def get_open_transactions(self):
        return self.open_transactions[:]

    def load_data(self):
        # on a utiliser pickling ( using pickle ) pour garder le mm type de donnée mais on doit
        # stocker les information en binaire mais on a paas besoin de overting the data we loaded from the file
        # les donnée resteront comme ils  sont
        # mais par contre le json nous donne les données en text alors il va supprimer qlq info
        # et du coup on doit les faire overite
        # alors pour convertire les donnée on a le choix de travailler avec json et avec pickle
        try:
            with open('blockchain.txt', mode='r') as f:
                # file_content = .loads(f.read())
                file_content = f.readlines()
                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                # we want to overite the transactions of each block of the blockchain
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(
                        tx['sender'], tx['recipient'],tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(
                        block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)

            self.chain = updated_blockchain
            #  WE MUST USE THE SAME TYPE OF DATA (si on a travailler avec the ordereddict alors il faut continuer avec )
            open_transactions = json.loads(file_content[1])
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = Transaction(
                    tx['sender'], tx['recipient'],tx['signature'], tx['amount'])
                updated_transactions.append(updated_transaction)

            self.open_transactions = updated_transactions

        except (IOError, IndexError):
            # error handlig
            print('handled exception...')
        except ValueError:
            print("A Value Error")
        except:
            print("All the other Errors")
        finally:
            # this allways execute
            print('Clean up !')

    def save_data(self):
        try:
            with open('blockchain.txt', mode="w") as f:
                """ JSON Syntaxe"""
                # for binary data we use the "wb" mode
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [
                    tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.open_transactions]
                f.write(json.dumps(saveable_tx))
                # Pickle syntaxe
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except:
            print("Saving failed")

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_util.hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balence(self):
        if self.hosting_node == None:
            return None
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions
                      if tx.sender == participant] for block in self.__chain]
        # il faut aussi enclure les donnée qui ne sont pas encole mined genre dans les open transactions
        open_tx_sender = [tx.amount
                          for tx in self.open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(lambda tx_sum, tx_amnt:  tx_sum + sum(tx_amnt)
                             if len(tx_amnt) > 0 else tx_sum + 0, tx_sender, 0)
        # amount_sent = 0
        # for tx in tx_sender:
        #     if len(tx) > 0:
        #         amount_sent += tx[0]
        tx_recipient = [[tx.amount for tx in block.transactions
                         if tx.recipient == participant] for block in self.__chain]
        #  WE USE THE REDUCE METHOD INSTEAD THE FOR LOOP
        amount_recived = reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount)
                                if len(tx_amount) > 0 else tx_sum + 0, tx_recipient, 0)
        # for tx in tx_recipient:
        #     if len(tx) > 0:
        #         amount_recived += tx[0]
        return amount_recived - amount_sent

    def get_last_blockchain_value(self):
        """Returns the last value of the blockchain"""
        # chekking if the blockchian is empty or not
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, recipient,sender,signature, amount=1.0):
        """Append a new value as the last value of the blockchain"""
        if self.hosting_node == None:
            return False
        transaction = Transaction(sender, recipient,signature, amount)
        if Verification.verify_transaction(transaction, self.get_balence):
            self.open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self):
        """Creating the Blocks"""
        # we are using the Dictionaries data structure
        if self.hosting_node == None:
            return None
        last_block = self.__chain[-1]  # acces the last element of the blockchain
        # join sert a joindre des elements d'une liste et les separer par la caractére specefier avant
        hashed_block = hash_util.hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction(
            'Mining', self.hosting_node,'',MINING_REWARDS)
        copied_open_transaction = self.open_transactions[:]
        for tx in copied_open_transaction:
            if not Wallet.verify_transaction(tx):
                return False
        copied_open_transaction.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block,
                      copied_open_transaction, proof)
        self.__chain.append(block)
        self.open_transactions = []
        self.save_data()
        return block
