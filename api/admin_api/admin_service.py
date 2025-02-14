import os
import subprocess
import sys
import psutil # type: ignore
import platform
from typing import Dict, Any


class AdminService:
    """Service for handling administrative tasks for the blockchain node."""

    @staticmethod
    def restart_node() -> Dict[str, str]:
        """
        Restarts the blockchain node.
        :return: A message indicating the node is restarting.
        """
        try:
            print("Restarting node...")
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_system_diagnostics() -> Dict[str, Any]:
        """
        Retrieves system diagnostics including CPU, memory, and disk usage.
        :return: A dictionary containing system diagnostic information.
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
            },
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }

    @staticmethod
    def manage_node(action: str) -> Dict[str, str]:
        """
        Manages node operations such as start, stop, or restart.
        :param action: The operation to perform (start, stop, restart).
        :return: A message indicating the result of the operation.
        """
        valid_actions = ["start", "stop", "restart"]
        if action not in valid_actions:
            return {"error": f"Invalid action. Valid actions are: {', '.join(valid_actions)}"}

        try:
            if action == "start":
                print("Starting the node...")
                # Assuming node is a separate process or service
                subprocess.Popen(["python", "node.py"])
                return {"message": "Node started successfully"}
            elif action == "stop":
                print("Stopping the node...")
                for proc in psutil.process_iter():
                    if "node.py" in proc.cmdline():
                        proc.terminate()
                        return {"message": "Node stopped successfully"}
                return {"error": "Node process not found"}
            elif action == "restart":
                print("Restarting the node...")
                AdminService.restart_node()
                return {"message": "Node is restarting"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def run_diagnostics() -> Dict[str, Any]:
        """
        Runs a full diagnostic check.
        :return: A dictionary containing system and process diagnostics.
        """
        return AdminService.get_system_diagnostics()


# Example usage
if __name__ == "__main__":
    admin_service = AdminService()

    # Perform some admin tasks
    print("System Diagnostics:")
    print(admin_service.get_system_diagnostics())

    print("\nManage Node - Start:")
    print(admin_service.manage_node("start"))

    print("\nManage Node - Stop:")
    print(admin_service.manage_node("stop"))

    print("\nDiagnostics:")
    print(admin_service.run_diagnostics())
