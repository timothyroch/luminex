import os
import json
import time
import requests # type: ignore
from pathlib import Path

# Configuration
NODES_DIR = "testnet/nodes"
LOG_DIR = "testnet/logs"
MONITOR_INTERVAL = 10  # seconds between checks
RPC_PORTS = [8545, 8546, 8547, 8548]  # RPC ports for each node
STATUS_FILE = "testnet_status.json"

def get_node_status(node_rpc_port):
    """
    Check the status of a node via its RPC port.
    """
    try:
        response = requests.post(
            f"http://localhost:{node_rpc_port}",
            json={"jsonrpc": "2.0", "method": "eth_syncing", "params": [], "id": 1},
            timeout=5
        )
        data = response.json()
        return {
            "rpc_port": node_rpc_port,
            "is_syncing": data["result"] if data["result"] else False,
            "status": "online"
        }
    except requests.exceptions.RequestException:
        return {"rpc_port": node_rpc_port, "is_syncing": None, "status": "offline"}

def get_block_height(node_rpc_port):
    """
    Get the current block height of a node via its RPC port.
    """
    try:
        response = requests.post(
            f"http://localhost:{node_rpc_port}",
            json={"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1},
            timeout=5
        )
        block_number = int(response.json()["result"], 16)
        return block_number
    except (requests.exceptions.RequestException, KeyError):
        return None

def monitor_nodes():
    """
    Monitor the health and synchronization status of all nodes.
    """
    status_data = {"nodes": []}
    for rpc_port in RPC_PORTS:
        node_status = get_node_status(rpc_port)
        block_height = get_block_height(rpc_port)
        node_status["block_height"] = block_height
        status_data["nodes"].append(node_status)

    # Save status data to a JSON file
    with open(STATUS_FILE, "w") as status_file:
        json.dump(status_data, status_file, indent=4)
    
    print("Current Testnet Status:")
    print(json.dumps(status_data, indent=4))

def log_status():
    """
    Log the status data to a log file.
    """
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    log_file = Path(LOG_DIR) / f"testnet_log_{timestamp}.json"
    with open(log_file, "w") as log:
        with open(STATUS_FILE, "r") as status:
            log.write(status.read())
    print(f"Status logged to {log_file}")

def main():
    """
    Main function to monitor and log testnet status at regular intervals.
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    while True:
        monitor_nodes()
        log_status()
        time.sleep(MONITOR_INTERVAL)

if __name__ == "__main__":
    main()
