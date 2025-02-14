import time
import requests # type: ignore
from multiprocessing import Process, Manager

NODE_URLS = [
    "http://node1:5000",
    "http://node2:5001",
    "http://node3:5002"
]

def broadcast_block(block_data, node_url):
    """Simulates broadcasting a block to a node."""
    try:
        response = requests.post(f"{node_url}/api/block", json=block_data, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

def measure_propagation_time(block_data, results):
    """Measures the time it takes for a block to propagate to all nodes."""
    start_times = {url: time.time() for url in NODE_URLS}
    for node_url in NODE_URLS:
        success = broadcast_block(block_data, node_url)
        if success:
            end_time = time.time()
            propagation_time = end_time - start_times[node_url]
            results[node_url] = propagation_time
        else:
            results[node_url] = None

if __name__ == "__main__":
    manager = Manager()
    results = manager.dict()

    # Simulate a new block
    block_data = {
        "index": 100,
        "previous_hash": "abc123",
        "timestamp": int(time.time()),
        "transactions": [{"sender": "Alice", "receiver": "Bob", "amount": 50}],
        "nonce": 12345,
        "hash": "def456"
    }

    print("Testing block propagation...")

    # Measure propagation times
    process = Process(target=measure_propagation_time, args=(block_data, results))
    process.start()
    process.join()

    # Report results
    for node_url, propagation_time in results.items():
        if propagation_time is not None:
            print(f"Node {node_url} received the block in {propagation_time:.2f} seconds.")
        else:
            print(f"Node {node_url} failed to receive the block.")
