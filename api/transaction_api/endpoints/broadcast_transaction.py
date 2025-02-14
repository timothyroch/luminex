from flask import Flask, request, jsonify # type: ignore
import requests # type: ignore
import time

app = Flask(__name__)

# In-memory peer node list (replace with a dynamic discovery system in production)
peer_nodes = [
    "http://node1.blockchain.net",
    "http://node2.blockchain.net",
    "http://node3.blockchain.net"
]

@app.route("/broadcast_transaction", methods=["POST"])
def broadcast_transaction():
    """
    API endpoint to broadcast a transaction to peer nodes.
    Expected JSON input:
    {
        "id": "transaction_id",
        "sender": "address1",
        "receiver": "address2",
        "amount": 50.0,
        "timestamp": 1673445600,
        "signature": "transaction_signature"
    }
    """
    transaction = request.json

    # Validate input
    required_fields = ["id", "sender", "receiver", "amount", "timestamp", "signature"]
    for field in required_fields:
        if field not in transaction:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Broadcast to peer nodes
    failed_nodes = []
    for node in peer_nodes:
        try:
            response = requests.post(f"{node}/receive_transaction", json=transaction, timeout=5)
            if response.status_code != 200:
                failed_nodes.append(node)
                print(f"Failed to broadcast to {node}. Response: {response.status_code}")
        except requests.exceptions.RequestException as e:
            failed_nodes.append(node)
            print(f"Error broadcasting to {node}: {e}")

    # Response summary
    if failed_nodes:
        return jsonify({
            "message": "Transaction broadcast partially successful.",
            "failed_nodes": failed_nodes
        }), 207
    else:
        return jsonify({"message": "Transaction broadcast successfully to all nodes."}), 200


if __name__ == "__main__":
    app.run(debug=True)
