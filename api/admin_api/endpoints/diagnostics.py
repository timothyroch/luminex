from flask import Flask, jsonify # type: ignore
import psutil # type: ignore
import platform
import time
import socket

app = Flask(__name__)

def get_system_info():
    """
    Retrieves general system information.
    :return: A dictionary containing system details.
    """
    return {
        "system": platform.system(),
        "node_name": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }


def get_resource_usage():
    """
    Retrieves resource usage statistics (CPU, memory, disk).
    :return: A dictionary containing CPU, memory, and disk usage.
    """
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return {
        "cpu_usage_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "total": f"{memory.total / (1024 ** 3):.2f} GB",
            "used": f"{memory.used / (1024 ** 3):.2f} GB",
            "available": f"{memory.available / (1024 ** 3):.2f} GB",
            "percent_used": f"{memory.percent}%"
        },
        "disk": {
            "total": f"{disk.total / (1024 ** 3):.2f} GB",
            "used": f"{disk.used / (1024 ** 3):.2f} GB",
            "free": f"{disk.free / (1024 ** 3):.2f} GB",
            "percent_used": f"{disk.percent}%"
        }
    }


def get_network_info():
    """
    Retrieves network information, including the hostname and IP address.
    :return: A dictionary containing network details.
    """
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return {
        "hostname": hostname,
        "ip_address": ip_address
    }


@app.route("/diagnostics", methods=["GET"])
def diagnostics():
    """
    API endpoint to retrieve detailed system and node diagnostics.
    :return: JSON response containing diagnostics information.
    """
    diagnostics_info = {
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
        "system_info": get_system_info(),
        "resource_usage": get_resource_usage(),
        "network_info": get_network_info()
    }
    return jsonify(diagnostics_info)


if __name__ == "__main__":
    print("Diagnostics API is running...")
    app.run(debug=True, port=5005)
