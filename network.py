from flask import request, jsonify, Flask

app = Flask(__name__)
nodes = {}
wallets = {}


@app.route("/add_node", methods=["POST"])
def add_node():
    json = request.get_json()
    address, url = json["address"], json["url"]

    nodes[address] = url
    return "registered", 200


@app.route("/add_wallet", methods=["POST"])
def add_wallet():
    json = request.get_json()
    address, url = json["address"], json["url"]

    wallets[address] = url
    return "registered", 200


@app.route("/remove_node", methods=["POST"])
def remove_node():
    json_request = request.get_json()
    uuid = json_request["uuid"]
    del nodes[uuid]
    return "node removed from the network", 200


@app.route("/remove_wallet", methods=["POST"])
def remove_wallet():
    json_request = request.get_json()
    pub_key = json_request["pub_key"]
    del wallets[pub_key]
    return "wallet removed from the network", 200


@app.route("/get_nodes", methods=["GET"])
def get_nodes():
    return jsonify(nodes)


@app.route("/get_wallets", methods=["GET"])
def get_wallets():
    return jsonify(wallets)


if __name__ == '__main__':
    app.run()
