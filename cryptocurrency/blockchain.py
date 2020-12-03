from datetime import datetime
from hashlib import sha256


class Transaction:

    def __init__(self, txn_hash=None, prev_hash=None, address=None, amount=0, fee=0, txn_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        self.txn_hash = txn_hash
        self.prev_hash = prev_hash
        self.address = address
        self.amount = amount
        self.fee = fee
        self.txn_time = txn_time

    def create_hash(self):
        self.txn_hash = sha256(str(self.__dict__).encode()).hexdigest()
        return self


class Block:

    def __init__(self, prev_hash, transactions=[], difficulty=4, timestamp=datetime.now()):
        self.difficulty = difficulty
        self.proof = 0
        self.hash = None
        self.prev_hash = prev_hash
        self.timestamp = str(timestamp)
        self.transactions = transactions

    def create_hash(self):
        block_string = str({
            "proof": self.proof,
            "timestamp": self.timestamp,
            "transactions": self.transactions
        })
        return sha256(block_string.encode()).hexdigest()

    def calculate(self):
        self.hash = self.create_hash()
        while not self.hash.startswith('0' * self.difficulty):
            self.proof += 1
            self.hash = self.create_hash()


class Blockchain:

    def __init__(self, chain=[]):
        self.chain = chain
        self.create_genesis()

    def create_genesis(self):
        block = Block("0")
        block.calculate()
        self.chain.append(block)

    def is_chain_valid(self):
        for index, block in enumerate(self.chain, start=1):
            if self.chain[index-1].txn_hash != block.txn_hash:
                return False
            if not block.txn_hash.startswith('0' * block.difficulty):
                return False
            if block.proof != block.create_hash():
                return False
        return True
