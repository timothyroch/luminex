import json
import random
import logging
from time import time
from threading import Thread
from blockchain.network.p2p_node import P2PNode

# Configure logging
logging.basicConfig(
    filename="monitoring/logs/gossip_protocol.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

class GossipProtocol:
    """Implements the Gossip Protocol for data dissemination in a P2P network."""

    def __init__(self, p2p_node, gossip_interval=5, redundancy=3):
        """
        Initializes the GossipProtocol.
        :param p2p_node: Instance of the P2PNode class for network communication.
        :param gossip_interval: Time interval (seconds) between successive gossips.
        :param redundancy: Number of peers to gossip with for each message.
        """
        self.node = p2p_node
        self.gossip_interval = gossip_interval
        self.redundancy = redundancy
        self.seen_messages = {}  # Store message hashes and their timestamps

    def _generate_message_id(self, message):
        """Generates a unique ID for a message using its content."""
        return hash(json.dumps(message, sort_keys=True))

    def send_gossip(self, message):
        """
        Gossips a message to a subset of peers.
        :param message: The message to gossip (e.g., block, transaction).
        """
        message_id = self._generate_message_id(message)
        if message_id in self.seen_messages:
            logging.info(f"Message already seen: {message_id}")
            return

        # Mark message as seen and propagate
        self.seen_messages[message_id] = time()
        peers = self.node.get_peers()
        if not peers:
            logging.warning("No peers available for gossip.")
            return

        # Select a random subset of peers
        selected_peers = random.sample(peers, min(self.redundancy, len(peers)))
        for peer in selected_peers:
            try:
                self.node.send_message(peer, {"type": "gossip", "data": message})
                logging.info(f"Gossiped message {message_id} to peer {peer}")
            except Exception as e:
                logging.error(f"Failed to gossip message to {peer}: {e}")

    def handle_incoming_message(self, message):
        """
        Handles an incoming gossip message.
        :param message: The received gossip message.
        """
        message_id = self._generate_message_id(message)
        if message_id in self.seen_messages:
            logging.info(f"Ignored duplicate message: {message_id}")
            return

        # Mark message as seen and propagate further
        self.seen_messages[message_id] = time()
        logging.info(f"Received new gossip message: {message_id}")
        self.send_gossip(message)

    def cleanup_seen_messages(self, expiration_time=300):
        """
        Removes old messages from the seen list to free up memory.
        :param expiration_time: Time (seconds) after which messages are removed.
        """
        current_time = time()
        to_remove = [msg_id for msg_id, timestamp in self.seen_messages.items() if current_time - timestamp > expiration_time]
        for msg_id in to_remove:
            del self.seen_messages[msg_id]
        logging.info(f"Cleaned up {len(to_remove)} old messages.")

    def start_gossiping(self):
        """Starts the gossip process in the background."""
        def gossip_loop():
            while True:
                self.cleanup_seen_messages()
                logging.info("Gossip loop running...")
                import time
                time.sleep(self.gossip_interval)

        gossip_thread = Thread(target=gossip_loop, daemon=True)
        gossip_thread.start()

# Example usage
if __name__ == "__main__":
    # Simulated P2P node for demonstration
    class DummyP2PNode:
        def get_peers(self):
            return ["node1:5001", "node2:5002", "node3:5003"]

        def send_message(self, peer, message):
            print(f"Sent message to {peer}: {message}")

    # Initialize GossipProtocol with a dummy P2PNode
    p2p_node = DummyP2PNode()
    gossip = GossipProtocol(p2p_node)

    # Start gossiping in the background
    gossip.start_gossiping()

    # Simulate sending a gossip message
    test_message = {"type": "block", "data": {"index": 5, "hash": "abc123", "transactions": []}}
    gossip.send_gossip(test_message)

    # Simulate receiving a gossip message
    incoming_message = {"type": "block", "data": {"index": 5, "hash": "abc123", "transactions": []}}
    gossip.handle_incoming_message(incoming_message)
