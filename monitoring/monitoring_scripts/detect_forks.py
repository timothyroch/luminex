import json
import requests # type: ignore
from datetime import datetime
from monitoring.alerts.alert_manager import AlertManager # type: ignore

# Load monitoring configuration
with open('monitoring/monitoring_config.json') as config_file:
    config = json.load(config_file)

NODE_URLS = config["node_urls"]  # List of node URLs to monitor
LOG_FILE = 'monitoring/logs/node_logs/fork_detection.log'

# Initialize alert manager
alert_manager = AlertManager()

def log_fork_details(fork_info):
    """Logs details about the detected fork."""
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{datetime.now()} - {fork_info}\n")

def fetch_latest_blocks():
    """Fetches the latest block data (index and hash) from all nodes."""
    latest_blocks = {}
    for node_url in NODE_URLS:
        try:
            response = requests.get(f"{node_url}/api/chain_overview", timeout=5)
            if response.status_code == 200:
                data = response.json()
                latest_blocks[node_url] = {
                    "index": data["total_blocks"] - 1,
                    "hash": data["latest_block_hash"]
                }
            else:
                print(f"Failed to fetch chain overview from {node_url}.")
        except requests.exceptions.RequestException:
            print(f"Node {node_url} is unreachable.")
    return latest_blocks

def detect_forks():
    """Detects forks by comparing block hashes across nodes."""
    latest_blocks = fetch_latest_blocks()
    fork_points = {}

    # Compare block hashes across nodes
    for node1, block1 in latest_blocks.items():
        for node2, block2 in latest_blocks.items():
            if node1 != node2 and block1["index"] == block2["index"] and block1["hash"] != block2["hash"]:
                print(f"Fork detected between {node1} and {node2} at block index {block1['index']}.")
                fork_points[(node1, node2)] = block1["index"]
                fork_info = {
                    "nodes": [node1, node2],
                    "block_index": block1["index"],
                    "hashes": [block1["hash"], block2["hash"]]
                }
                log_fork_details(fork_info)
                alert_manager.trigger_alert(
                    f"Fork detected between {node1} and {node2} at block index {block1['index']}."
                )

    if not fork_points:
        print("No forks detected.")
    else:
        print(f"Fork points detected: {fork_points}")

if __name__ == "__main__":
    detect_forks()
