from flask import Flask, jsonify # type: ignore
import random
import time

app = Flask(__name__)

# Simulated blockchain sync status
BLOCKCHAIN_INFO = {
    "current_block": 10500,  # Current block height of this node
    "network_block": 10510,  # Latest block height in the network
    "sync_start_time": time.time() - 600,  # Sync started 10 minutes ago
}


def get_sync_status():
    """
    Calculates the synchronization status of the node.
    :return: A dictionary containing sync status details.
    """
    current_block = BLOCKCHAIN_INFO["current_block"]
    network_block = BLOCKCHAIN_INFO["network_block"]
    blocks_behind = max(0, network_block - current_block)

    status = {
        "current_block": current_block,
        "network_block": network_block,
        "blocks_behind": blocks_behind,
        "sync_percentage": calculate_sync_percentage(current_block, network_block),
        "sync_status": "synced" if blocks_behind == 0 else "syncing",
        "time_since_sync_started": human_readable_time(int(time.time() - BLOCKCHAIN_INFO["sync_start_time"]))
    }

    return status


def calculate_sync_percentage(current_block: int, network_block: int) -> float:
    """
    Calculates the sync progress as a percentage.
    :param current_block: Current block height of the node.
    :param network_block: Latest block height in the network.
    :return: Sync percentage.
    """
    if network_block == 0:
        return 100.0  # Prevent division by zero
    return (current_block / network_block) * 100


def human_readable_time(seconds: int) -> str:
    """
    Converts seconds into a human-readable time format.
    :param seconds: Time in seconds.
    :return: A human-readable string (e.g., "10m 20s").
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes}m {seconds}s" if hours else f"{minutes}m {seconds}s"


@app.route("/block_sync_status", methods=["GET"])
def block_sync_status():
    """
    API endpoint to retrieve the synchronization status of the node.
    :return: JSON response containing block sync status.
    """
    status = get_sync_status()
    return jsonify(status)


if __name__ == "__main__":
    # Simulate block synchronization for demonstration purposes
    def simulate_sync():
        while True:
            if BLOCKCHAIN_INFO["current_block"] < BLOCKCHAIN_INFO["network_block"]:
                BLOCKCHAIN_INFO["current_block"] += random.randint(1, 3)  # Simulate syncing blocks
            time.sleep(2)

    import threading
    threading.Thread(target=simulate_sync, daemon=True).start()

    app.run(debug=True, port=5001)
