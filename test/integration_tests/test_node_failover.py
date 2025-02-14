import unittest
import time
import requests # type: ignore
from multiprocessing import Process

NODE_URLS = ["http://node1:5000", "http://node2:5001", "http://node3:5002"]
TRANSACTION_API = "/api/transaction"
BLOCKCHAIN_API = "/api/chain"

class TestNodeFailover(unittest.TestCase):
    def setUp(self):
        """Prepare the test environment by submitting some initial transactions."""
        self.initial_transactions = [
            {"sender": "Alice", "receiver": "Bob", "amount": 50},
            {"sender": "Charlie", "receiver": "Dave", "amount": 30}
        ]
        for transaction in self.initial_transactions:
            response = requests.post(f"{NODE_URLS[0]}{TRANSACTION_API}", json=transaction)
            self.assertEqual(response.status_code, 200, "Failed to submit initial transactions")

    def simulate_node_failure(self, node_url):
        """Simulates a node failure by stopping its process."""
        # This assumes the node is running in a separate script or container
        print(f"Simulating failure for {node_url}...")
        # Implementation depends on your setup (e.g., stopping a Docker container or process)

    def recover_node(self, node_url):
        """Simulates recovering a failed node."""
        print(f"Recovering {node_url}...")
        # Implementation depends on your setup (e.g., restarting a Docker container or process)

    def test_failover_and_recovery(self):
        """Tests failover handling when a node goes offline and recovers."""
        failed_node = NODE_URLS[1]

        # Submit transactions before failure
        response = requests.post(f"{NODE_URLS[0]}{TRANSACTION_API}", json={"sender": "Eve", "receiver": "Frank", "amount": 20})
        self.assertEqual(response.status_code, 200, "Failed to submit transaction before node failure")

        # Simulate node failure
        self.simulate_node_failure(failed_node)

        # Submit more transactions while the node is offline
        response = requests.post(f"{NODE_URLS[0]}{TRANSACTION_API}", json={"sender": "Gina", "receiver": "Henry", "amount": 15})
        self.assertEqual(response.status_code, 200, "Failed to submit transaction during node failure")

        # Recover the failed node
        self.recover_node(failed_node)
        time.sleep(5)  # Wait for the node to sync

        # Verify the recovered node is synchronized
        response = requests.get(f"{failed_node}{BLOCKCHAIN_API}")
        self.assertEqual(response.status_code, 200, "Failed to retrieve blockchain from recovered node")
        recovered_chain = response.json()["chain"]
        live_chain = requests.get(f"{NODE_URLS[0]}{BLOCKCHAIN_API}").json()["chain"]
        self.assertEqual(recovered_chain, live_chain, "Recovered node's chain is not synchronized with the network")

if __name__ == "__main__":
    unittest.main()
