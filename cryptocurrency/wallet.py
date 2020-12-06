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

    def sign_txn(self, b_message):
        signature = self.priv_key.sign(b_message, self.signature_algorithm)
        return signature.hex()

    def verify_signature(self, message):
        try:
            self.wallet.pub_key.verify(self.signature, message, self.signature_algorithm)
            return True
        except InvalidSignature:
            return False

    def transfer_utxn(self, address, amount):
        if self.balance > amount:
            input_utxn_balance = 0
            input_utxns = []
            new_utxn = None
            for utxn in self.utxns:
                input_utxns.append(utxn)
                input_utxn_balance += utxn.amount

                if input_utxn_balance >= amount:
                    new_utxn = Transaction(prev_hash=[utxn.txn_hash for utxn in input_utxns],
                                           address=address,
                                           amount=amount).create_hash()
                    new_utxn.signature = self.sign_txn(new_utxn.to_bytes())

                if input_utxn_balance > amount:
                    rest_utxn = Transaction(prev_hash=[utxn.txn_hash],
                                            address=self.address,
                                            amount=input_utxn_balance-amount).create_hash()
                    rest_utxn.signature = self.sign_txn(rest_utxn.to_bytes())
                    self.utxns.append(rest_utxn)
                if new_utxn:
                    break
            for input_utxn in input_utxns:
                self.utxns.remove(input_utxn)

        return new_utxn
