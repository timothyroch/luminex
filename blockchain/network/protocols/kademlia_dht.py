import hashlib
import random
import json
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(
    filename="monitoring/logs/kademlia_dht.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

class KademliaDHT:
    """Implements the Kademlia Distributed Hash Table for peer discovery and data storage."""

    def __init__(self, node_id, k=20, alpha=3):
        """
        Initializes the Kademlia DHT.
        :param node_id: The unique ID of this node.
        :param k: Number of contacts to keep in each bucket (bucket size).
        :param alpha: Number of parallel queries during lookups.
        """
        self.node_id = node_id
        self.k = k
        self.alpha = alpha
        self.routing_table = defaultdict(list)  # Buckets of peers organized by distance
        self.data_store = {}  # Key-value store for DHT data

    def _distance(self, id1, id2):
        """Calculates the XOR distance between two node IDs."""
        return int(id1, 16) ^ int(id2, 16)

    def _bucket_index(self, node_id):
        """Determines which bucket a node belongs to based on its distance from this node."""
        distance = self._distance(self.node_id, node_id)
        return distance.bit_length() - 1

    def add_peer(self, node_id, address):
        """
        Adds a peer to the appropriate bucket in the routing table.
        :param node_id: The ID of the peer.
        :param address: The network address of the peer.
        """
        bucket_index = self._bucket_index(node_id)
        bucket = self.routing_table[bucket_index]

        # Avoid duplicate entries
        for peer in bucket:
            if peer["node_id"] == node_id:
                return

        # Maintain bucket size
        if len(bucket) < self.k:
            bucket.append({"node_id": node_id, "address": address})
            logging.info(f"Added peer {node_id} to bucket {bucket_index}")
        else:
            logging.warning(f"Bucket {bucket_index} is full. Cannot add peer {node_id}")

    def find_closest_peers(self, key):
        """
        Finds the closest peers to a given key in the DHT.
        :param key: The key to search for.
        :return: A list of the closest peers.
        """
        target_distance = self._distance(self.node_id, key)
        all_peers = [
            peer for bucket in self.routing_table.values() for peer in bucket
        ]
        sorted_peers = sorted(all_peers, key=lambda peer: self._distance(peer["node_id"], key))
        return sorted_peers[:self.k]

    def store_data(self, key, value):
        """
        Stores a key-value pair in the DHT.
        :param key: The key under which the value is stored.
        :param value: The value to store.
        """
        self.data_store[key] = value
        logging.info(f"Stored data: {key} -> {value}")

    def retrieve_data(self, key):
        """
        Retrieves a value from the DHT for a given key.
        :param key: The key to look up.
        :return: The corresponding value, or None if the key is not found.
        """
        return self.data_store.get(key, None)

    def iterative_lookup(self, key):
        """
        Performs an iterative lookup for a key in the DHT.
        :param key: The key to search for.
        :return: The closest value or closest peers to the key.
        """
        closest_peers = self.find_closest_peers(key)
        queried_peers = set()

        for _ in range(self.alpha):
            for peer in closest_peers:
                if peer["node_id"] in queried_peers:
                    continue
                queried_peers.add(peer["node_id"])
                # Simulate querying the peer
                logging.info(f"Querying peer {peer['node_id']} for key {key}")
                # Normally, you'd send a network request here

        return closest_peers

    def hash_key(self, data):
        """
        Generates a 160-bit hash of the data for use as a DHT key.
        :param data: The data to hash.
        :return: The hexadecimal hash of the data.
        """
        return hashlib.sha1(data.encode("utf-8")).hexdigest()


# Example usage
if __name__ == "__main__":
    # Initialize the DHT with a node ID
    my_node_id = hashlib.sha1(b"my_node").hexdigest()
    dht = KademliaDHT(node_id=my_node_id)

    # Add peers to the routing table
    for i in range(5):
        peer_id = hashlib.sha1(f"peer{i}".encode("utf-8")).hexdigest()
        dht.add_peer(peer_id, f"peer{i}.example.com:500{i}")

    # Store and retrieve data
    key = dht.hash_key("some_key")
    dht.store_data(key, "some_value")
    print("Retrieved data:", dht.retrieve_data(key))

    # Find closest peers to a key
    closest_peers = dht.find_closest_peers(key)
    print("Closest peers:", closest_peers)

    # Perform an iterative lookup
    lookup_result = dht.iterative_lookup(key)
    print("Lookup result:", lookup_result)
