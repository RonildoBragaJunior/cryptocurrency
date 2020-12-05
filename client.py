import json

import requests
from flask import request, Flask, jsonify

from cryptocurrency.blockchain import Transaction
from cryptocurrency.node import Node

headers = {"Content-Type": "application/json"}
app = Flask(__name__)
local_node = Node()


@app.route("/register", methods=["GET"])
def register():
    local_address = {"address": request.url_root}
    response = requests.post("http://localhost:8000/add_node",
                             data=json.dumps(local_address),
                             headers=headers)

    if response.status_code == 200:
        registered_nodes = response.json()["nodes"]
        for registered_node in registered_nodes:
            if registered_node != local_address["address"]:
                local_node.network_nodes.append(registered_node)
        return "registered", 200


@app.route("/add_node", methods=["POST"])
def add_node():
    json_request = request.get_json()
    node_address = json_request["address"]
    local_node.network_nodes.append(node_address)
    return "node registered", 200


@app.route("/add_utxn", methods=["POST"])
def add_utxn():
    data = request.get_json()
    transaction = Transaction(**data)

    local_node.add_utxn(transaction)
    return "transaction received", 200


@app.route("/get_utxns", methods=["GET"])
def get_utxns():
    data = [utxn.__dict__ for utxn in local_node.utxns]
    return jsonify(data), 200


@app.route("/mine_utxns", methods=["GET"])
def mine_utxns():
    local_node.mine_utxns()
    return "New block mined", 200


@app.route("/get_blockchain", methods=["GET"])
def get_blockchain():
    chain = jsonify(local_node.blockchain.to_json())
    return chain, 200


@app.route("/check_network_blockchain", methods=["GET"])
def check_network_blockchains():
    biggest_chain = local_node.compare_chains()
    result = {"chain": biggest_chain.chain, "length": len(biggest_chain.chain)}
    return result, 200


if __name__ == '__main__':
    app.run()
