import psutil # type: ignore
import time
from prometheus_client import start_http_server, Gauge # type: ignore

class NodeMetrics:
    def __init__(self):
        # Define Prometheus metrics
        self.cpu_usage_gauge = Gauge("node_cpu_usage_percent", "CPU usage percentage per node")
        self.memory_usage_gauge = Gauge("node_memory_usage_percent", "Memory usage percentage per node")
        self.disk_usage_gauge = Gauge("node_disk_usage_percent", "Disk usage percentage per node")
        self.uptime_gauge = Gauge("node_uptime_seconds", "Node uptime in seconds")

    def collect_cpu_usage(self):
        """
        Collects the CPU usage percentage.
        """
        cpu_usage = psutil.cpu_percent(interval=1)
        self.cpu_usage_gauge.set(cpu_usage)
        return cpu_usage

    def collect_memory_usage(self):
        """
        Collects the memory usage percentage.
        """
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
        self.memory_usage_gauge.set(memory_usage)
        return memory_usage

    def collect_disk_usage(self):
        """
        Collects the disk usage percentage.
        """
        disk_info = psutil.disk_usage("/")
        disk_usage = disk_info.percent
        self.disk_usage_gauge.set(disk_usage)
        return disk_usage

    def collect_uptime(self):
        """
        Collects the node uptime in seconds.
        """
        uptime = time.time() - psutil.boot_time()
        self.uptime_gauge.set(uptime)
        return uptime

    def export_metrics(self):
        """
        Continuously collects and exports node metrics.
        """
        while True:
            cpu = self.collect_cpu_usage()
            memory = self.collect_memory_usage()
            disk = self.collect_disk_usage()
            uptime = self.collect_uptime()

            print(f"CPU Usage: {cpu}% | Memory Usage: {memory}% | Disk Usage: {disk}% | Uptime: {uptime}s")
            time.sleep(10)  # Adjust the collection interval as needed

if __name__ == "__main__":
    # Start Prometheus HTTP server on port 8000
    start_http_server(8000)
    print("Starting Node Metrics Exporter on port 8000...")

    metrics = NodeMetrics()
    metrics.export_metrics()
