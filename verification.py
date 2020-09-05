import hash_util


class Verification:
    #valid proof n'utilise aucun attribue ou fonction de la class donc elle peut etre une static method
    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        guess = (str([tx.to_ordered_dict for tx in transactions]) +
                 str(last_hash) + str(proof)).encode()
        guess_hash = hash_util.hash_string_256(guess)
        # on peut spicifier n'import quelle condition
        return guess_hash[0:2] == "00"

    @classmethod
    def verify_chain(cls, blockchain):
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_util.hash_block(blockchain[index-1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                return False
        return True
    @staticmethod
    def verify_transaction(transaction, get_balence):
        sender_balance = get_balence()
        return sender_balance >= transaction.amount
    @classmethod
    def verify_transactions(cls, open_transactions, get_balence):
        return all([cls.verify_transaction(tx, get_balence) for tx in open_transactions])
