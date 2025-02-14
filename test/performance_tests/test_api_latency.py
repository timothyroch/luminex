import unittest
import time
import requests # type: ignore
from concurrent.futures import ThreadPoolExecutor

class TestAPILatency(unittest.TestCase):
    BASE_URL = "http://localhost:5000/api"  # Replace with actual base URL of your API

    def measure_latency(self, endpoint):
        """
        Measure the response time of an API endpoint.
        """
        start_time = time.time()
        response = requests.get(f"{self.BASE_URL}/{endpoint}")
        elapsed_time = time.time() - start_time
        return elapsed_time, response.status_code

    def test_transaction_api_latency(self):
        """
        Measure latency for the transaction API.
        """
        latency, status_code = self.measure_latency("transaction_api/create_transaction")
        self.assertEqual(status_code, 200, "Transaction API returned an error")
        self.assertLess(latency, 1, "Transaction API latency exceeds acceptable threshold")
        print(f"Transaction API latency: {latency:.3f}s")

    def test_explorer_api_latency(self):
        """
        Measure latency for the block explorer API.
        """
        latency, status_code = self.measure_latency("explorer_api/query_block")
        self.assertEqual(status_code, 200, "Explorer API returned an error")
        self.assertLess(latency, 1, "Explorer API latency exceeds acceptable threshold")
        print(f"Explorer API latency: {latency:.3f}s")

    def test_healthcheck_api_latency(self):
        """
        Measure latency for the healthcheck API.
        """
        latency, status_code = self.measure_latency("healthcheck_api/node_status")
        self.assertEqual(status_code, 200, "Healthcheck API returned an error")
        self.assertLess(latency, 1, "Healthcheck API latency exceeds acceptable threshold")
        print(f"Healthcheck API latency: {latency:.3f}s")

    def test_latency_under_concurrent_load(self):
        """
        Measure latency for a single endpoint under concurrent load.
        """
        endpoint = "transaction_api/create_transaction"

        def make_request():
            latency, status_code = self.measure_latency(endpoint)
            self.assertEqual(status_code, 200, "API returned an error under load")
            return latency

        with ThreadPoolExecutor(max_workers=10) as executor:
            latencies = list(executor.map(make_request, range(10)))

        avg_latency = sum(latencies) / len(latencies)
        self.assertLess(avg_latency, 1.5, "Average latency under load exceeds acceptable threshold")
        print(f"Average latency under concurrent load: {avg_latency:.3f}s")

if __name__ == "__main__":
    unittest.main()
