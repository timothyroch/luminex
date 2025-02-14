import json
import requests # type: ignore
from datetime import datetime
from monitoring.alerts.alert_manager import AlertManager # type: ignore

# Load monitoring configuration
with open('monitoring/monitoring_config.json') as config_file:
    config = json.load(config_file)

NODE_URLS = config["node_urls"]  # List of node URLs to monitor
LOG_FILE = 'monitoring/logs/node_logs/node_status.log'
ALERT_THRESHOLD = config["alert_threshold"]  # Number of consecutive failures before alerting

# Initialize alert manager
alert_manager = AlertManager()

# Track failure counts for each node
failure_counts = {url: 0 for url in NODE_URLS}

def log_status(node_url, status):
    """Logs the status of a node to the log file."""
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{datetime.now()} - {node_url} - {status}\n")

def check_node_status():
    """Checks the status of each node."""
    for node_url in NODE_URLS:
        try:
            response = requests.get(f"{node_url}/health/node_status", timeout=5)
            if response.status_code == 200:
                print(f"Node {node_url} is online.")
                log_status(node_url, "online")
                failure_counts[node_url] = 0  # Reset failure count
            else:
                print(f"Node {node_url} is offline.")
                log_status(node_url, "offline")
                failure_counts[node_url] += 1
        except requests.exceptions.RequestException:
            print(f"Node {node_url} is unreachable.")
            log_status(node_url, "unreachable")
            failure_counts[node_url] += 1

        # Trigger alert if failures exceed the threshold
        if failure_counts[node_url] >= ALERT_THRESHOLD:
            alert_manager.trigger_alert(
                f"Node {node_url} has been offline for {failure_counts[node_url]} consecutive checks."
            )

if __name__ == "__main__":
    check_node_status()
