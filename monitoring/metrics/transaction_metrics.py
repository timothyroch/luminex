import random
import time
from prometheus_client import start_http_server, Gauge # type: ignore

class TransactionMetrics:
    def __init__(self):
        # Define Prometheus metrics
        self.tps_gauge = Gauge("blockchain_tps", "Transactions per second (TPS)")
        self.avg_confirmation_time_gauge = Gauge("blockchain_avg_confirmation_time", "Average transaction confirmation time in seconds")
        self.pending_tx_gauge = Gauge("blockchain_pending_transactions", "Number of pending transactions in the queue")

    def collect_tps(self):
        """
        Simulates collection of TPS (Transactions Per Second).
        Replace this with actual data from the blockchain.
        """
        tps = random.uniform(5, 100)  # Simulating TPS
        self.tps_gauge.set(tps)
        return tps

    def collect_avg_confirmation_time(self):
        """
        Simulates collection of average transaction confirmation time.
        Replace this with actual data from the blockchain.
        """
        avg_confirmation_time = random.uniform(0.5, 5.0)  # Simulating confirmation time
        self.avg_confirmation_time_gauge.set(avg_confirmation_time)
        return avg_confirmation_time

    def collect_pending_transactions(self):
        """
        Simulates collection of pending transactions.
        Replace this with actual data from the transaction pool.
        """
        pending_transactions = random.randint(0, 500)  # Simulating pending transactions
        self.pending_tx_gauge.set(pending_transactions)
        return pending_transactions

    def export_metrics(self):
        """
        Continuously collects and exports transaction metrics.
        """
        while True:
            tps = self.collect_tps()
            avg_time = self.collect_avg_confirmation_time()
            pending_tx = self.collect_pending_transactions()

            print(f"TPS: {tps:.2f} | Avg Confirmation Time: {avg_time:.2f}s | Pending Transactions: {pending_tx}")
            time.sleep(10)  # Adjust the collection interval as needed

if __name__ == "__main__":
    # Start Prometheus HTTP server on port 8001
    start_http_server(8001)
    print("Starting Transaction Metrics Exporter on port 8001...")

    metrics = TransactionMetrics()
    metrics.export_metrics()
