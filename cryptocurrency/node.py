import json
from uuid import uuid4

import requests

import tools
from cryptocurrency.blockchain import Blockchain, Block


class Node:
    def __init__(self, node_address=str(uuid4()), reward_address=str(uuid4()), utxns=[]):
        self.node_address = node_address
        self.reward_address = reward_address
        self.utxns = utxns
        self.blockchain = Blockchain()
        self.network_nodes = {}

    def add_utxn(self, transaction):
        self.utxns.append(transaction)

        # announce transaction on the network
        # for node_address in self.network_nodes:
        #     requests.post(node_address + "/add_block",
        #                   data=transaction.to_json(),
        #                   headers=constant.HEADERS)

    def mine_utxns(self):
        if len(self.utxns) > 0:
            new_block = Block(prev_hash=self.blockchain.chain[-1].hash, transactions=self.utxns.copy())
            self.utxns = []
            new_block.calculate()

            self.blockchain.chain.append(new_block)

            # announce mined block on the network
            for network_node in self.network_nodes:
                node_url = self.network_nodes[network_node]
                data = {"block": new_block.to_json()}
                requests.post(node_url + "/add_block", data=json.dumps(data), headers=tools.HEADERS)

    def compare_chains(self):
        for node_address in self.network_nodes:
            response = requests.get(node_address + "/chain")
            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]

                new_blockchain = Blockchain(chain)
                if length > len(self.blockchain.chain) and new_blockchain.is_chain_valid():
                    self.blockchain.chain = new_blockchain

        return self.blockchain.chain
