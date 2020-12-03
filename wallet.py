import json

import requests
from flask import request, Flask, jsonify

from cryptocurrency.blockchain import Transaction
from cryptocurrency.wallet import Wallet

headers = {"Content-Type": "application/json"}
app = Flask(__name__)
wallet = Wallet()
nodes = []


@app.route("/add_utxn", methods=["POST"])
def add_utxn():
    json_request = request.get_json()
    utxn = Transaction(address=wallet.address, amount=json_request["amount"]).create_hash()
    wallet.utxns.append(utxn)

    return "ok", 200


@app.route("/get_utxns", methods=["GET"])
def get_utxns():
    result = jsonify([utxn.__dict__ for utxn in wallet.utxns])
    return result, 200


@app.route("/move_utxn", methods=["POST"])
def move_utxn():
    json_received = request.get_json()
    address, amount = json_received["address"], json_received["amount"]
    new_txn = wallet.calculate_transfer(address, amount)

    response = requests.get("http://localhost:8000/get_nodes")
    if response.status_code == 200:
        registered_nodes = response.json()["nodes"]
        for node in registered_nodes:
            requests.post(
                node + "/add_transaction",
                data=json.dumps(new_txn.__dict__),
                headers=headers
            )

    return "ok", 200


if __name__ == '__main__':
    app.run()
