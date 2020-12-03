import uuid

from cryptocurrency.blockchain import Transaction


class Wallet:

    def __init__(self, address=str(uuid.uuid4()), utxns=[]):
        self.address = address
        self.utxns = utxns

    def move_transaction(self, input_txns, new_address, amount):
        new_txn, rest_txn = None, None
        prev_hash = []

        for input_txn in input_txns:
            prev_hash.append(input_txn.txn_hash)

            if input_txn.amount > amount:
                new_txn = Transaction(prev_hash=prev_hash,
                                      address=new_address,
                                      amount=amount).create_hash()
                if input_txn.amount - amount > 0:
                    rest_txn = Transaction(prev_hash=[input_txn.txn_hash],
                                           address=self.address,
                                           amount=input_txn.amount - amount).create_hash()
            else:
                amount -= input_txn.amount

        return new_txn, rest_txn

    def calculate_transfer(self, address, amount):
        input_tx, total_input = [], 0

        for index in range(0, len(self.utxns)):
            input_tx.append(self.utxns[index])
            total_input += self.utxns[index].amount
            if total_input >= amount:
                new_transaction, rest_transaction = self.move_transaction(input_tx, address, amount)
                if rest_transaction:
                    self.utxns.append(rest_transaction)
                return new_transaction
