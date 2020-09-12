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
import requests

# Exports

from utility import hash_util

MINING_REWARDS = 10

print(__name__)


class Blockchain():
    def __init__(self, public_key, node_id):
        # Initializing the empty blockchain
        genesis_block = Block(0, '', [], 100, 0)
        # on peut declarer chain et open_transactions comme des attribute privé
        self.chain = [genesis_block]
        # for the inhandle transactions
        self.open_transactions = []
        self.public_key = public_key
        self.node_id = node_id
        self.peer_nodes = set()
        self.resolve_conflits = False
        self.load_data()

    # Getters

    @property
    def chain(self):
        return self.__chain[:]
    # Setters

    @chain.setter
    def chain(self, value):
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
            with open('blockchain-{}.txt'.format(self.node_id), mode='r') as f:
                # file_content = .loads(f.read())
                file_content = f.readlines()
                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                # we want to overite the transactions of each block of the blockchain
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(
                        block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)

                self.chain = updated_blockchain
                #  WE MUST USE THE SAME TYPE OF DATA (si on a travailler avec the ordereddict alors il faut continuer avec )
                print("akramou" + file_content[2])
                peer_nodes = json.loads(file_content[2])
                self.peer_nodes = set(peer_nodes)
                updated_transactions = []
                open_transactions = json.loads(file_content[1])[:-1]
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
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
            with open('blockchain-{}.txt'.format(self.node_id), mode="w") as f:
                """ JSON Syntaxe"""
                # for binary data we use the "wb" mode
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [
                    tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.open_transactions]
                f.write(json.dumps(saveable_tx))
                f.write('\n')
                f.write(json.dumps(list(self.peer_nodes)))

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

    def get_balence(self, sender=None):
        if sender == None:
            if self.public_key == None:
                return None
            participant = self.public_key
        else:
            participant = sender
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

    def add_transaction(self, recipient, sender, signature, amount=1.0, is_reciving=False):
        """Append a new value as the last value of the blockchain
        :is_reciving: to know if we are adding a transaction or broadcasting to another node
        """

        # if self.public_key == None:
        #     return False
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balence):
            self.open_transactions.append(transaction)
            self.save_data()
            if not is_reciving:
                for node in self.peer_nodes:
                    url = 'http://{}/broadcast-transaction'.format(node)
                    try:
                        response = requests.post(url, json={
                            "sender": sender, "recipient": recipient, "amount": amount, "signature": signature})
                        if response.status_code == 400 or response.status_code == 500:
                            print("transaction declined, need resolving")
                            return False
                        if response.status_code == 409:
                            self.resolve_conflits = True
                    except requests.exceptions.ConnectionError:
                        continue
            return True
        return False

    def mine_block(self):
        """Creating the Blocks"""
        # we are using the Dictionaries data structure
        if self.public_key == None:
            return None
        # acces the last element of the blockchain
        last_block = self.__chain[-1]
        # join sert a joindre des elements d'une liste et les separer par la caractére specefier avant
        hashed_block = hash_util.hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction(
            'Mining', self.public_key, '', MINING_REWARDS)
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
        for node in self.peer_nodes:
            url = "http://{}/broadcast-block".format(node)
            converted_block = block.__dict__.copy()
            converted_block['transactions'] = [
                tx.__dict__ for tx in converted_block['transactions']]
            try:
                response = requests.post(url, json={'block': converted_block})
                print("thie status code is : {}".format(response.status_code))
                if response.status_code == 400 or response.status_code == 500:
                    print("transaction declined, need resolving")
                    return False
                if response.status_code == 409:
                    self.resolve_conflits = True
            except requests.exceptions.ConnectionError:
                continue

        return block

    def add_peer_node(self, node):
        self.peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        self.peer_nodes.discard(node)
        self.save_data()

    def get_all_nodes(self):
        print(self.peer_nodes)
        return list(self.peer_nodes)

    def add_block(self, block):
        transactions = [Transaction(
            tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
        proof_is_valid = Verification.valid_proof(
            transactions[:-1], block['previous_hash'], block['proof'])
        # print(proof_is_valid)
        # we check if the hash of the last block is equal with the previous_hash of the incomming block
        hashes_match = hash_util.hash_block(
            self.chain[-1]) == block['previous_hash']
        print(hashes_match)
        if not hashes_match or not proof_is_valid:
            return False
        converted_block = Block(
            block['index'], block['previous_hash'], transactions, block['proof'], block['timestamp'])
        self.__chain.append(converted_block)
        stored_transactions = self.open_transactions[:]
        for itx in block['transactions']:
            for opentx in stored_transactions:
                if opentx.sender == itx['sender'] and opentx.recipient == itx['recipient'] and opentx.amount == itx['amount'] and opentx.signature == itx['signature']:
                    # remove all the transactions that are redendent (dans le premier et le 2eme serveur)
                    try:
                        self.open_transactions.remove(opentx)
                    except ValueError:
                        print('item was already removed')
        self.save_data()
        return True

    def resolve(self):
        winner_chain = self.chain
        replace = False
        for node in self.peer_nodes:
            url = "http://{}/chain".format(node)
            try:
                response = requests.get(url)
                node_chain = response.json()
                node_chain = [Block(
                    block['index'],
                    block['previous_hash'],
                    [Transaction(tx['sender'], tx['recipient'], tx['signature'],
                                 tx['amount']) for tx in block['transactions']],
                    block['proof'],
                    block['timestamp']) for block in node_chain]
                node_chain_length = len(node_chain)
                local_chain_length = len(winner_chain)
                if node_chain_length > local_chain_length and Verification.verify_chain(node_chain):
                    winner_chain = node_chain
            except requests.exceptions.ConnectionError:
                continue
        self.resolve_conflits = False
        self.chain = winner_chain
        if replace:
            self.open_transactions = []
        self.save_data()
        return replace
