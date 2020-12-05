import json
import uuid

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

from cryptocurrency.blockchain import Transaction


class Wallet:
    curve = ec.SECP256R1()
    signature_algorithm = ec.ECDSA(hashes.SHA256())
    private_value = 0x63bd3b01c5ce749d87f5f7481232a93540acdb0f7b5c014ecd9cd32b041d6f33

    def __init__(self, address=str(uuid.uuid4()), utxns=[]):
        self.priv_key = ec.derive_private_key(self.private_value, self.curve, default_backend())
        self.pub_key = self.priv_key.public_key()
        self.address = address
        self.utxns = utxns

    @property
    def balance(self):
        balance = 0
        for utxn in self.utxns:
            balance += utxn.amount
        return balance

    def sign_txn(self, txn):
        message = json.dumps(txn.__dict__)
        b_message = bytes(message, 'utf-8')
        signature = self.priv_key.sign(b_message, self.signature_algorithm)
        txn.signature = signature.hex()

    def verify_signature(self, message):
        try:
            self.wallet.pub_key.verify(self.signature, message, self.signature_algorithm)
            return True
        except InvalidSignature:
            return False

    def transfer_utxn(self, address, amount):
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
                    self.utxns.append(Transaction(prev_hash=[utxn.txn_hash],
                                                  address=self.address,
                                                  amount=input_utxn_balance-amount).create_hash())

                if new_utxn or rest_utxn:
                    break

        return new_utxn