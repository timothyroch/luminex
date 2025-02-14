from prometheus_client import start_http_server, Gauge, Counter # type: ignore
import psutil # type: ignore
import time
from transactions.transaction_pool import TransactionPool
from blocks.blockchain_state import Blockchain

# Prometheus metrics
tps_metric = Counter("transaction_throughput", "Number of transactions processed per second")
block_time_metric = Gauge("block_creation_time", "Time taken to create a block in seconds")
cpu_usage_metric = Gauge("cpu_usage", "CPU usage percentage")
memory_usage_metric = Gauge("memory_usage", "Memory usage percentage")
blockchain_size_metric = Gauge("blockchain_size", "Number of blocks in the blockchain")

# Initialize blockchain and transaction pool
blockchain = Blockchain()
transaction_pool = TransactionPool()

def collect_system_metrics():
    """Collects CPU and memory usage."""
    cpu_usage_metric.set(psutil.cpu_percent())
    memory_usage_metric.set(psutil.virtual_memory().percent)

def simulate_block_creation():
    """Simulates block creation and measures time taken."""
    start_time = time.time()
    # Simulate block mining (dummy transactions for demonstration)
    pending_transactions = transaction_pool.get_pending_transactions(max_count=10)
    new_block = blockchain.create_block(pending_transactions)
    blockchain.add_block(new_block, difficulty=2)
    end_time = time.time()

    # Update metrics
    block_time_metric.set(end_time - start_time)
    blockchain_size_metric.set(len(blockchain.chain))
    tps_metric.inc(len(pending_transactions))

def start_prometheus_exporter(port=8000):
    """Starts the Prometheus metrics exporter."""
    print(f"Starting Prometheus exporter on port {port}...")
    start_http_server(port)
    while True:
        collect_system_metrics()
        time.sleep(1)  # Collect system metrics every second

if __name__ == "__main__":
    # Start Prometheus metrics server
    start_prometheus_exporter()

    # Simulate block creation every 10 seconds for testing
    while True:
        simulate_block_creation()
        time.sleep(10)
