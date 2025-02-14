import unittest
import time
import requests # type: ignore

NODE_URLS = ["http://node1:5000", "http://node2:5001", "http://node3:5002"]
CHAIN_API = "/api/chain"
NEW_BLOCK_API = "/api/block"

class TestBlockSyncing(unittest.TestCase):
    def create_new_block(self, node_url, block_data):
        """Sends a new block to a node."""
        response = requests.post(f"{node_url}{NEW_BLOCK_API}", json=block_data)
        return response.status_code == 200

    def get_chain(self, node_url):
        """Fetches the blockchain from a node."""
        response = requests.get(f"{node_url}{CHAIN_API}")
        if response.status_code == 200:
            return response.json()["chain"]
        return None

    def test_block_synchronization(self):
        """Tests that all nodes synchronize to the same chain after a new block is added."""
        # Create a new block on node1
        block_data = {
            "index": 5,
            "previous_hash": "abc123",
            "timestamp": int(time.time()),
            "transactions": [{"sender": "Alice", "receiver": "Bob", "amount": 50}],
            "nonce": 12345,
            "hash": "def456"
        }
        result = self.create_new_block(NODE_URLS[0], block_data)
        self.assertTrue(result, "Failed to create new block on node1")

        # Wait for synchronization
        time.sleep(5)

        # Check that all nodes have the same chain
        chains = [self.get_chain(node_url) for node_url in NODE_URLS]
        for chain in chains:
            self.assertEqual(chain, chains[0], "Blockchain is not synchronized across nodes")

    def test_fork_resolution(self):
        """Tests that nodes resolve forks by adopting the longest valid chain."""
        # Simulate a fork by creating different chains on node1 and node2
        block_data_node1 = {
            "index": 5,
            "previous_hash": "abc123",
            "timestamp": int(time.time()),
            "transactions": [{"sender": "Charlie", "receiver": "Dave", "amount": 20}],
            "nonce": 11111,
            "hash": "ghi789"
        }
        block_data_node2 = {
            "index": 5,
            "previous_hash": "abc123",
            "timestamp": int(time.time()),
            "transactions": [{"sender": "Eve", "receiver": "Frank", "amount": 30}],
            "nonce": 22222,
            "hash": "jkl012"
        }

        # Add conflicting blocks to node1 and node2
        self.create_new_block(NODE_URLS[0], block_data_node1)
        self.create_new_block(NODE_URLS[1], block_data_node2)

        # Add a new block to node1 to extend its chain
        extended_block = {
            "index": 6,
            "previous_hash": "ghi789",
            "timestamp": int(time.time()),
            "transactions": [{"sender": "Alice", "receiver": "Bob", "amount": 10}],
            "nonce": 33333,
            "hash": "mno345"
        }
        self.create_new_block(NODE_URLS[0], extended_block)

        # Wait for synchronization
        time.sleep(10)

        # Verify that all nodes adopt the longest valid chain
        chains = [self.get_chain(node_url) for node_url in NODE_URLS]
        for chain in chains:
            self.assertEqual(chain, chains[0], "Fork resolution failed: nodes have different chains")

if __name__ == "__main__":
    unittest.main()
