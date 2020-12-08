from uuid import uuid4

import requests
from cryptocurrency.blockchain import Transaction, Blockchain, Block


class Node:
    def __init__(self, node_address=str(uuid4()), reward_address=str(uuid4()), utxns=[]):
        self.node_address = node_address
        self.reward_address = reward_address
        self.utxns = utxns
        self.blockchain = Blockchain()
        self.network_nodes = {}

    def mine_utxns(self):
        if len(self.utxns) > 0:
            new_block = Block(prev_hash=self.blockchain.chain[-1].hash, txns=self.utxns.copy())
            self.utxns = []
            new_block.calculate()

            self.blockchain.chain.append(new_block)
            self.compare_chains()

    def compare_chains(self):
        for node_address in self.network_nodes:
            response = requests.get(self.network_nodes[node_address] + "blockchain")
            if response.status_code == 200:
                blockchain = []

                for block in response.json()["chain"]:
                    txns = block["txns"]
                    block["txns"] = [Transaction(**txn) for txn in txns]
                    blockchain.append(Block(**block))

                if len(blockchain) > len(self.blockchain.chain):
                    self.blockchain.chain = blockchain

        return self.blockchain.chain
