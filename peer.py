import json
import time
import requests
from flask import request, Flask, jsonify
import threading
import tools
from cryptocurrency.blockchain import Transaction
from cryptocurrency.node import Node

app = Flask(__name__)
local_node = Node()


def mine():
    while True:
        print("mining")
        local_node.mine_utxns()
        time.sleep(10)


@app.route("/register", methods=["GET"])
def register():
    data = {"address": local_node.node_address, "url": request.url_root}
    requests.post(tools.lighthouse + "add_node",
                  data=json.dumps(data),
                  headers=tools.HEADERS)
    return "local network nodes updated", 200


@app.route("/update_network", methods=["GET"])
def update_network():
    response = requests.get(tools.lighthouse + "get_nodes")
    global_network_nodes = response.json()
    for global_network_node in global_network_nodes:
        if not tools.my_url(global_network_nodes[global_network_node]):
            local_node.network_nodes[global_network_node] = global_network_nodes[global_network_node]
    return "local network nodes updated", 200


@app.route("/get_network", methods=["GET"])
def get_network():
    data = jsonify(local_node.network_nodes)
    return data, 200


@app.route("/add_utxn", methods=["POST"])
def add_utxn():
    data = request.get_json()
    transaction = Transaction(**data)
    local_node.utxns.append(transaction)
    return "transaction received", 200


@app.route("/get_utxns", methods=["GET"])
def get_utxns():
    data = [utxn.__dict__ for utxn in local_node.utxns]
    return jsonify(data), 200


@app.route("/mine_utxns", methods=["GET"])
def mine_utxns():
    local_node.mine_utxns()
    return "New block mined", 200


@app.route("/blockchain", methods=["GET"])
def blockchain():
    chain = jsonify(local_node.blockchain.to_json())
    return chain, 200


@app.route("/check_network_blockchain", methods=["GET"])
def check_network_blockchains():
    biggest_chain = local_node.compare_chains()
    result = {"chain": biggest_chain.chain, "length": len(biggest_chain.chain)}
    return result, 200


@app.before_first_request
def before_first_request_func():
    x = threading.Thread(target=mine)
    x.start()


if __name__ == '__main__':
    app.run()
