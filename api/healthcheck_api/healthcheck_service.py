import psutil # type: ignore
import time
import requests # type: ignore
from typing import Dict, Any, List, Optional

class HealthCheckService:
    """Service for performing node and network health checks."""

    def __init__(self, peer_nodes: List[str]):
        self.peer_nodes = peer_nodes
        self.node_start_time = time.time()

    def get_node_status(self) -> Dict[str, Any]:
        """
        Retrieves the status and resource usage of the node.
        :return: A dictionary containing node status details.
        """
        uptime_seconds = int(time.time() - self.node_start_time)
        process = psutil.Process()

        status = {
            "status": "running",
            "uptime": self.human_readable_time(uptime_seconds),
            "cpu_usage": f"{psutil.cpu_percent()}%",
            "memory_usage": f"{process.memory_info().rss / (1024 ** 2):.2f} MB",
            "disk_usage": self.get_disk_usage()
        }
        return status

    def get_disk_usage(self) -> Dict[str, str]:
        """
        Retrieves disk usage statistics.
        :return: A dictionary containing disk usage information.
        """
        disk = psutil.disk_usage('/')
        return {
            "total": f"{disk.total / (1024 ** 3):.2f} GB",
            "used": f"{disk.used / (1024 ** 3):.2f} GB",
            "free": f"{disk.free / (1024 ** 3):.2f} GB",
            "percent_used": f"{disk.percent}%"
        }

    def get_block_sync_status(self, current_block: int, network_block: int) -> Dict[str, Any]:
        """
        Calculates the synchronization status of the node.
        :param current_block: The current block height of the node.
        :param network_block: The latest block height in the network.
        :return: A dictionary containing sync status details.
        """
        blocks_behind = max(0, network_block - current_block)
        return {
            "current_block": current_block,
            "network_block": network_block,
            "blocks_behind": blocks_behind,
            "sync_percentage": self.calculate_sync_percentage(current_block, network_block),
            "sync_status": "synced" if blocks_behind == 0 else "syncing"
        }

    def calculate_sync_percentage(self, current_block: int, network_block: int) -> float:
        """
        Calculates the synchronization progress as a percentage.
        :param current_block: Current block height of the node.
        :param network_block: Latest block height in the network.
        :return: Sync percentage.
        """
        if network_block == 0:
            return 100.0  # Prevent division by zero
        return (current_block / network_block) * 100

    def check_peer_node_health(self, node_url: str) -> Dict[str, Any]:
        """
        Checks the health of a peer node by measuring its latency and availability.
        :param node_url: The URL of the peer node.
        :return: A dictionary containing the health status of the node.
        """
        start_time = time.time()
        try:
            response = requests.get(f"{node_url}/ping", timeout=3)
            latency = time.time() - start_time
            return {
                "node_url": node_url,
                "status": "online" if response.status_code == 200 else "offline",
                "latency_ms": round(latency * 1000, 2)
            }
        except requests.exceptions.RequestException:
            return {
                "node_url": node_url,
                "status": "offline",
                "latency_ms": None
            }

    def get_network_health(self) -> Dict[str, Any]:
        """
        Retrieves the health status of all peer nodes in the network.
        :return: A dictionary containing the overall network health.
        """
        network_health = [self.check_peer_node_health(node) for node in self.peer_nodes]
        overall_status = "healthy" if all(node["status"] == "online" for node in network_health) else "degraded"
        return {
            "overall_status": overall_status,
            "node_count": len(self.peer_nodes),
            "healthy_nodes": sum(1 for node in network_health if node["status"] == "online"),
            "unhealthy_nodes": sum(1 for node in network_health if node["status"] == "offline"),
            "details": network_health
        }

    def human_readable_time(self, seconds: int) -> str:
        """
        Converts seconds into a human-readable time format.
        :param seconds: Time in seconds.
        :return: A human-readable string (e.g., "1h 2m 3s").
        """
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours}h {minutes}m {seconds}s" if hours else f"{minutes}m {seconds}s"


# Example usage
if __name__ == "__main__":
    # Simulated peer nodes
    peer_nodes = [
        "http://node1.blockchain.net",
        "http://node2.blockchain.net",
        "http://node3.blockchain.net"
    ]

    health_service = HealthCheckService(peer_nodes)

    # Get node status
    print("Node Status:")
    print(health_service.get_node_status())

    # Get block sync status
    print("\nBlock Sync Status:")
    print(health_service.get_block_sync_status(current_block=10500, network_block=10510))

    # Get network health
    print("\nNetwork Health:")
    print(health_service.get_network_health())
