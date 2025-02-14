import time
from typing import Dict, Any, List, Optional


def human_readable_time(seconds: int) -> str:
    """
    Converts seconds into a human-readable time format.
    :param seconds: Time in seconds.
    :return: A human-readable string (e.g., "1h 2m 3s").
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes}m {seconds}s" if hours else f"{minutes}m {seconds}s"


def format_disk_usage(disk_usage: Dict[str, float]) -> Dict[str, str]:
    """
    Formats disk usage statistics for better readability.
    :param disk_usage: A dictionary containing raw disk usage stats in bytes.
    :return: A formatted dictionary with human-readable disk usage stats.
    """
    return {
        "total": f"{disk_usage['total'] / (1024 ** 3):.2f} GB",
        "used": f"{disk_usage['used'] / (1024 ** 3):.2f} GB",
        "free": f"{disk_usage['free'] / (1024 ** 3):.2f} GB",
        "percent_used": f"{disk_usage['percent']}%"
    }


def format_node_status(status: Dict[str, Any]) -> Dict[str, Any]:
    """
    Formats the node status for better readability.
    :param status: Raw node status data.
    :return: A formatted dictionary containing node status details.
    """
    return {
        "Status": status.get("status", "unknown").capitalize(),
        "Uptime": status.get("uptime"),
        "CPU Usage": status.get("cpu_usage"),
        "Memory Usage": status.get("memory_usage"),
        "Disk Usage": status.get("disk_usage")
    }


def format_network_health(health_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Formats the network health details for better readability.
    :param health_data: Raw network health data.
    :return: A formatted dictionary with network health information.
    """
    formatted_details = [
        {
            "Node URL": node["node_url"],
            "Status": node["status"].capitalize(),
            "Latency (ms)": node["latency_ms"] if node["latency_ms"] is not None else "N/A"
        }
        for node in health_data["details"]
    ]
    
    return {
        "Overall Status": health_data["overall_status"].capitalize(),
        "Total Nodes": health_data["node_count"],
        "Healthy Nodes": health_data["healthy_nodes"],
        "Unhealthy Nodes": health_data["unhealthy_nodes"],
        "Node Details": formatted_details
    }


def calculate_average_latency(nodes: List[Dict[str, Any]]) -> Optional[float]:
    """
    Calculates the average latency of online nodes in the network.
    :param nodes: A list of node health dictionaries.
    :return: The average latency in milliseconds, or None if no nodes are online.
    """
    latencies = [node["latency_ms"] for node in nodes if node["latency_ms"] is not None]
    return round(sum(latencies) / len(latencies), 2) if latencies else None
