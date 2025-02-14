import socket
import json
import logging
from threading import Thread

# Configure logging
logging.basicConfig(filename="monitoring/logs/node_discovery.log", level=logging.INFO, format="%(asctime)s - %(message)s")

class NodeDiscovery:
    """Handles the discovery and management of peers in the blockchain network."""

    def __init__(self, config_file="blockchain/network/network_config.json"):
        """
        Initializes the NodeDiscovery class by loading configuration.
        :param config_file: Path to the JSON configuration file.
        """
        with open(config_file) as file:
            self.config = json.load(file)
        self.port = self.config["port"]
        self.seed_nodes = self.config["seed_nodes"]
        self.connection_timeout = self.config["connection_timeout"]
        self.peers = set()

    def discover_peers(self):
        """Discovers peers by connecting to seed nodes and querying their peer lists."""
        for seed in self.seed_nodes:
            try:
                peer_list = self.query_peer_list(seed)
                self.peers.update(peer_list)
                logging.info(f"Discovered peers from {seed}: {peer_list}")
            except Exception as e:
                logging.error(f"Failed to connect to seed node {seed}: {e}")

    def query_peer_list(self, seed_node):
        """
        Queries a seed node for its list of known peers.
        :param seed_node: Address of the seed node (e.g., "node1.example.com:5000").
        :return: List of peers discovered from the seed node.
        """
        host, port = seed_node.split(":")
        port = int(port)
        with socket.create_connection((host, port), timeout=self.connection_timeout) as conn:
            message = {"type": "node_info_request"}
            conn.sendall(json.dumps(message).encode("utf-8"))
            response = conn.recv(4096).decode("utf-8")
            peer_list = json.loads(response).get("peers", [])
            return peer_list

    def broadcast_own_info(self):
        """Broadcasts this node's information to all connected peers."""
        own_info = {"type": "node_info", "data": {"address": f"localhost:{self.port}"}}
        for peer in self.peers:
            try:
                self.send_message(peer, own_info)
                logging.info(f"Broadcasted own info to {peer}")
            except Exception as e:
                logging.error(f"Failed to broadcast to {peer}: {e}")

    def send_message(self, peer, message):
        """
        Sends a message to a peer.
        :param peer: Address of the peer (e.g., "node2.example.com:5001").
        :param message: The message to send as a dictionary.
        """
        host, port = peer.split(":")
        port = int(port)
        with socket.create_connection((host, port), timeout=self.connection_timeout) as conn:
            conn.sendall(json.dumps(message).encode("utf-8"))

    def start_peer_discovery(self):
        """Continuously discovers new peers in the background."""
        def discovery_loop():
            while True:
                try:
                    self.discover_peers()
                    self.broadcast_own_info()
                except Exception as e:
                    logging.error(f"Error in peer discovery loop: {e}")
                finally:
                    import time
                    time.sleep(self.config.get("discovery_interval", 30))

        discovery_thread = Thread(target=discovery_loop, daemon=True)
        discovery_thread.start()

    def get_peers(self):
        """Returns the current list of known peers."""
        return list(self.peers)


# Example usage
if __name__ == "__main__":
    node_discovery = NodeDiscovery()

    # Start peer discovery in the background
    node_discovery.start_peer_discovery()

    # Wait for some peers to be discovered
    import time
    time.sleep(10)

    # Print discovered peers
    print("Discovered peers:", node_discovery.get_peers())
