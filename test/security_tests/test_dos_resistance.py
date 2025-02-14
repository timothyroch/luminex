import unittest
import time
import requests # type: ignore
from multiprocessing import Pool

NODE_URL = "http://localhost:5000"  # Replace with your node's URL
ENDPOINT = "/api/transaction"  # Example endpoint to test
MAX_REQUESTS = 500  # Total number of requests to simulate
RATE_LIMIT = 50  # Expected maximum requests per second

def send_request():
    """Sends a single request to the node."""
    try:
        transaction = {
            "sender": "Alice",
            "receiver": "Bob",
            "amount": 10
        }
        response = requests.post(f"{NODE_URL}{ENDPOINT}", json=transaction, timeout=5)
        return response.status_code
    except requests.exceptions.RequestException:
        return None

class TestDoSResistance(unittest.TestCase):
    def test_high_request_volume(self):
        """Simulates high request volume and checks system stability."""
        start_time = time.time()
        with Pool(10) as pool:  # Use 10 parallel workers
            statuses = pool.map(lambda _: send_request(), range(MAX_REQUESTS))
        end_time = time.time()

        # Calculate requests per second (RPS)
        elapsed_time = end_time - start_time
        rps = MAX_REQUESTS / elapsed_time

        # Ensure rate limiting is enforced
        self.assertLessEqual(rps, RATE_LIMIT, f"RPS exceeded the limit: {rps:.2f}")

        # Verify successful responses
        success_count = statuses.count(200)
        self.assertGreater(success_count, 0, "No successful requests")
        print(f"Completed {success_count}/{MAX_REQUESTS} requests in {elapsed_time:.2f} seconds. RPS: {rps:.2f}")

    def test_malformed_requests(self):
        """Sends malformed requests and ensures they are rejected."""
        malformed_data = {"sender": "Alice"}  # Missing required fields
        response = requests.post(f"{NODE_URL}{ENDPOINT}", json=malformed_data, timeout=5)
        self.assertNotEqual(response.status_code, 200, "Malformed request was incorrectly accepted")

if __name__ == "__main__":
    unittest.main()
