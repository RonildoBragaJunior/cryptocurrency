from flask import request, jsonify, Flask

app = Flask(__name__)
nodes = []


@app.route("/add_node", methods=["POST"])
def add_node():
    json = request.get_json()
    address = json["address"]

    if address not in nodes:
        nodes.append(str(address))

    response = {
        "length": len(nodes),
        "nodes": nodes
    }

    return jsonify(response), 200


@app.route("/remove_node", methods=["POST"])
def remove_node():
    json_request = request.get_json()
    node_address = json_request["address"]
    if node_address in nodes:
        nodes.remove(node_address)
        return "node removed to the network", 200
    else:
        return "this node was not registered", 200


@app.route("/get_nodes", methods=["GET"])
def get_nodes():
    return jsonify({
        "length": len(nodes),
        "nodes": nodes
    })


if __name__ == '__main__':
    app.run()
