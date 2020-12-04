import uuid

from cryptocurrency.blockchain import Transaction


class Wallet:

    def __init__(self, address=str(uuid.uuid4()), utxns=[]):
        self.address = address
        self.utxns = utxns

    @property
    def balance(self):
        balance = 0
        for utxn in self.utxns:
            balance += utxn.amount

        return balance

    def calculate_transfer(self, address, amount):
        new_utxn, rest_utxn = None, None
        if self.balance > amount:
            input_utxn_balance = 0
            input_utxn = []
            for utxn in self.utxns:
                input_utxn.append(utxn)
                input_utxn_balance += utxn.amount

                if input_utxn_balance >= amount:
                    new_utxn = Transaction(prev_hash=[utxn.txn_hash for utxn in input_utxn],
                                           address=address,
                                           amount=amount).create_hash()
                if input_utxn_balance > amount:
                    rest_utxn = Transaction(prev_hash=[utxn.txn_hash],
                                            address=self.address,
                                            amount=input_utxn_balance-amount).create_hash()
        return new_utxn, rest_utxn

