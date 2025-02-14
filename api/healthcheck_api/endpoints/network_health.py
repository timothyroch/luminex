from flask import Flask, jsonify # type: ignore
import requests # type: ignore
import time
import random

app = Flask(__name__)

# Simulated list of peer nodes
PEER_NODES = [
    "http://node1.blockchain.net",
    "http://node2.blockchain.net",
    "http://node3.blockchain.net"
]

def check_node_health(node_url: str) -> dict:
    """
    Checks the health of a peer node by measuring latency and availability.
    :param node_url: The URL of the peer node.
    :return: A dictionary containing the health status of the node.
    """
    start_time = time.time()
    try:
        response = requests.get(f"{node_url}/ping", timeout=3)  # Assuming a `/ping` endpoint exists on the peer node
        latency = time.time() - start_time
        return {
            "node_url": node_url,
            "status": "online" if response.status_code == 200 else "offline",
            "latency_ms": round(latency * 1000, 2)
        }
    except requests.exceptions.RequestException:
        return {
            "node_url": node_url,
            "status": "offline",
            "latency_ms": None
        }


def get_network_health():
    """
    Retrieves the health status of all peer nodes in the network.
    :return: A list of dictionaries containing the health status of each node.
    """
    network_health = [check_node_health(node) for node in PEER_NODES]
    overall_status = "healthy" if all(node["status"] == "online" for node in network_health) else "degraded"
    return {
        "overall_status": overall_status,
        "node_count": len(PEER_NODES),
        "healthy_nodes": sum(1 for node in network_health if node["status"] == "online"),
        "unhealthy_nodes": sum(1 for node in network_health if node["status"] == "offline"),
        "details": network_health
    }


@app.route("/network_health", methods=["GET"])
def network_health():
    """
    API endpoint to retrieve the health status of the network.
    :return: JSON response containing network health details.
    """
    status = get_network_health()
    return jsonify(status)


# Simulated `/ping` endpoint for testing purposes
@app.route("/ping", methods=["GET"])
def ping():
    """
    Simulates a /ping endpoint for health checks.
    """
    return jsonify({"message": "Pong!"}), 200


if __name__ == "__main__":
    # Simulate peer node behavior for demonstration
    def simulate_peer_nodes():
        while True:
            # Simulate random network changes (e.g., nodes going offline/online)
            if random.random() < 0.1:
                PEER_NODES.append(f"http://node{len(PEER_NODES) + 1}.blockchain.net")
            time.sleep(10)

    import threading
    threading.Thread(target=simulate_peer_nodes, daemon=True).start()

    app.run(debug=True, port=5002)
