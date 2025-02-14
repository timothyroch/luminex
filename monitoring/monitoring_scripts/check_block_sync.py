import json
import requests # type: ignore
from datetime import datetime
from monitoring.alerts.alert_manager import AlertManager # type: ignore

# Load monitoring configuration
with open('monitoring/monitoring_config.json') as config_file:
    config = json.load(config_file)

NODE_URLS = config["node_urls"]  # List of node URLs to monitor
LOG_FILE = 'monitoring/logs/node_logs/block_sync.log'
SYNC_THRESHOLD = config["sync_threshold"]  # Allowed difference in block height before triggering an alert

# Initialize alert manager
alert_manager = AlertManager()

def log_sync_status(node_url, status):
    """Logs the synchronization status of a node."""
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{datetime.now()} - {node_url} - {status}\n")

def get_latest_block_from_network():
    """Fetches the latest block index and hash from the network."""
    latest_block = {"index": -1, "hash": ""}
    for node_url in NODE_URLS:
        try:
            response = requests.get(f"{node_url}/api/chain_overview", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data["total_blocks"] > latest_block["index"]:
                    latest_block = {
                        "index": data["total_blocks"] - 1,
                        "hash": data["latest_block_hash"]
                    }
        except requests.exceptions.RequestException:
            print(f"Failed to fetch chain overview from {node_url}.")
    return latest_block

def check_block_sync():
    """Checks block synchronization status for each node."""
    latest_block = get_latest_block_from_network()

    for node_url in NODE_URLS:
        try:
            response = requests.get(f"{node_url}/api/chain_overview", timeout=5)
            if response.status_code == 200:
                data = response.json()
                node_index = data["total_blocks"] - 1
                node_hash = data["latest_block_hash"]

                if node_index < latest_block["index"] - SYNC_THRESHOLD:
                    print(f"Node {node_url} is out of sync.")
                    log_sync_status(node_url, "out_of_sync")
                    alert_manager.trigger_alert(
                        f"Node {node_url} is out of sync. Latest block index: {node_index}, Network block index: {latest_block['index']}."
                    )
                elif node_hash != latest_block["hash"]:
                    print(f"Node {node_url} has a mismatched block hash.")
                    log_sync_status(node_url, "hash_mismatch")
                    alert_manager.trigger_alert(
                        f"Node {node_url} has a hash mismatch. Node hash: {node_hash}, Network hash: {latest_block['hash']}."
                    )
                else:
                    print(f"Node {node_url} is synchronized.")
                    log_sync_status(node_url, "synchronized")
            else:
                print(f"Node {node_url} returned an error.")
                log_sync_status(node_url, "error")
        except requests.exceptions.RequestException:
            print(f"Node {node_url} is unreachable.")
            log_sync_status(node_url, "unreachable")

if __name__ == "__main__":
    check_block_sync()
