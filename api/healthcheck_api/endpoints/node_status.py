from flask import Flask, jsonify # type: ignore
import os
import time
import psutil # type: ignore

app = Flask(__name__)

# Node start time (used to calculate uptime)
NODE_START_TIME = time.time()


def get_node_status():
    """
    Retrieves the status and uptime of the node.
    :return: A dictionary containing node status information.
    """
    uptime_seconds = int(time.time() - NODE_START_TIME)
    process = psutil.Process(os.getpid())

    status = {
        "status": "running",
        "uptime": human_readable_time(uptime_seconds),
        "cpu_usage": f"{psutil.cpu_percent()}%",
        "memory_usage": f"{process.memory_info().rss / (1024 ** 2):.2f} MB",
        "disk_usage": get_disk_usage(),
    }

    return status


def get_disk_usage():
    """
    Retrieves disk usage statistics.
    :return: A dictionary containing disk usage information.
    """
    disk = psutil.disk_usage('/')
    return {
        "total": f"{disk.total / (1024 ** 3):.2f} GB",
        "used": f"{disk.used / (1024 ** 3):.2f} GB",
        "free": f"{disk.free / (1024 ** 3):.2f} GB",
        "percent_used": f"{disk.percent}%",
    }


def human_readable_time(seconds: int) -> str:
    """
    Converts seconds into a human-readable time format.
    :param seconds: Time in seconds.
    :return: A human-readable string (e.g., "1d 2h 3m 4s").
    """
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    parts = [
        f"{days}d" if days else "",
        f"{hours}h" if hours else "",
        f"{minutes}m" if minutes else "",
        f"{seconds}s" if seconds else "",
    ]
    return " ".join(filter(bool, parts))


@app.route("/node_status", methods=["GET"])
def node_status():
    """
    API endpoint to retrieve the status and uptime of the node.
    :return: JSON response containing node status.
    """
    status = get_node_status()
    return jsonify(status)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
