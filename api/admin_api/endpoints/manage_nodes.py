from flask import Flask, request, jsonify # type: ignore

app = Flask(__name__)

# In-memory list of peer nodes (for demonstration purposes)
PEER_NODES = [
    "http://node1.blockchain.net",
    "http://node2.blockchain.net",
    "http://node3.blockchain.net"
]


@app.route("/nodes", methods=["GET"])
def list_nodes():
    """
    Lists all the nodes in the network.
    :return: JSON response containing the list of nodes.
    """
    return jsonify({
        "message": "List of peer nodes",
        "nodes": PEER_NODES,
        "total_nodes": len(PEER_NODES)
    })


@app.route("/nodes/add", methods=["POST"])
def add_node():
    """
    Adds a new node to the network.
    :return: JSON response indicating success or failure.
    """
    data = request.get_json()
    new_node = data.get("node_url")

    if not new_node:
        return jsonify({"error": "Node URL is required"}), 400

    if new_node in PEER_NODES:
        return jsonify({"error": "Node already exists"}), 400

    PEER_NODES.append(new_node)
    return jsonify({
        "message": "Node added successfully",
        "node": new_node,
        "total_nodes": len(PEER_NODES)
    })


@app.route("/nodes/remove", methods=["POST"])
def remove_node():
    """
    Removes a node from the network.
    :return: JSON response indicating success or failure.
    """
    data = request.get_json()
    node_to_remove = data.get("node_url")

    if not node_to_remove:
        return jsonify({"error": "Node URL is required"}), 400

    if node_to_remove not in PEER_NODES:
        return jsonify({"error": "Node not found"}), 404

    PEER_NODES.remove(node_to_remove)
    return jsonify({
        "message": "Node removed successfully",
        "node": node_to_remove,
        "total_nodes": len(PEER_NODES)
    })


if __name__ == "__main__":
    app.run(debug=True, port=5003)
