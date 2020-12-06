import json
import tools
import requests
from flask import request, Flask, jsonify

from cryptocurrency.blockchain import Transaction
from cryptocurrency.wallet import Wallet

app = Flask(__name__)
wallet = Wallet()
nodes = []


@app.route("/register", methods=["GET"])
def register():
    local_address = {"address": wallet.address, "url": request.url_root,}
    requests.post(tools.lighthouse + "add_wallet",
                  data=json.dumps(local_address),
                  headers=tools.HEADERS)


@app.route("/add_utxn", methods=["POST"])
def add_utxn():
    json_request = request.get_json()
    utxn = Transaction(address=wallet.address, amount=json_request["amount"]).create_hash()
    utxn.signature = wallet.sign_txn(utxn.to_bytes())
    wallet.utxns.append(utxn)
    return "ok", 200


@app.route("/verify_signature", methods=["POST"])
def verify_signature():
    json_request = request.get_json()
    message = json_request["message"]
    if wallet.verify_signature(message):
        return "true", 200
    else:
        return "false", 200


@app.route("/get_utxns", methods=["GET"])
def get_utxns():
    result = jsonify([utxn.__dict__ for utxn in wallet.utxns])
    return result, 200


@app.route("/move_utxn", methods=["POST"])
def move_utxn():
    json_received = request.get_json()
    address, amount = json_received["address"], json_received["amount"]
    new_utxn = wallet.transfer_utxn(address, amount)

    response = requests.get("http://localhost:8000/get_nodes")
    if response.status_code == 200:
        registered_nodes = response.json()
        for node in registered_nodes:
            requests.post(
                registered_nodes[node] + "/add_utxn",
                data=json.dumps(new_utxn.__dict__),
                headers=tools.HEADERS
            )

    return "ok", 200


@app.before_first_request
def before_first_request_func():
    register()


if __name__ == '__main__':
    app.run()
