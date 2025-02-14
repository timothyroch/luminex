import json
import time
import requests # type: ignore
from datetime import datetime
from monitoring.alerts.alert_manager import AlertManager # type: ignore

# Load monitoring configuration
with open('monitoring/monitoring_config.json') as config_file:
    config = json.load(config_file)

NODE_URLS = config["node_urls"]
LATENCY_THRESHOLD = config.get("latency_threshold", 200)  # Threshold in milliseconds
LOG_FILE = "monitoring/logs/network_latency.log"

# Initialize alert manager
alert_manager = AlertManager()

def log_latency(node_url, latency):
    """Logs the latency of a node."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()} - Node: {node_url}, Latency: {latency} ms\n")

def measure_latency(node_url):
    """Measures the latency to a specific node."""
    try:
        start_time = time.time()
        response = requests.get(f"{node_url}/health/node_status", timeout=5)
        end_time = time.time()
        if response.status_code == 200:
            latency = (end_time - start_time) * 1000  # Convert to milliseconds
            return latency
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def monitor_network_latency():
    """Monitors the latency of all nodes and logs the results."""
    for node_url in NODE_URLS:
        latency = measure_latency(node_url)
        if latency is not None:
            log_latency(node_url, latency)
            print(f"Node {node_url} latency: {latency:.2f} ms")
            if latency > LATENCY_THRESHOLD:
                alert_manager.trigger_alert(
                    f"High latency detected for {node_url}: {latency:.2f} ms (Threshold: {LATENCY_THRESHOLD} ms)"
                )
        else:
            log_latency(node_url, "Unreachable")
            alert_manager.trigger_alert(f"Node {node_url} is unreachable.")

if __name__ == "__main__":
    print("Monitoring network latency...")
    while True:
        monitor_network_latency()
        time.sleep(60)  # Monitor every 60 seconds
