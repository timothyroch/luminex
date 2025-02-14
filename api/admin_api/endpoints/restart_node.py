from flask import Flask, jsonify # type: ignore
import os
import signal
import sys
import time

app = Flask(__name__)

@app.route("/restart", methods=["POST"])
def restart_node():
    """
    API endpoint to restart the blockchain node.
    :return: JSON response indicating the restart status.
    """
    try:
        # Log the restart request
        print("Restart request received. Preparing to restart the node...")

        # Send a response to indicate restart is in progress
        response = {
            "message": "Node is restarting...",
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        }

        # Schedule the restart after the response is sent
        time.sleep(2)  # Give time for the response to be sent
        os.kill(os.getpid(), signal.SIGINT)

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/status", methods=["GET"])
def status():
    """
    API endpoint to check the current status of the node.
    :return: JSON response indicating the node status.
    """
    return jsonify({
        "message": "Node is running",
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    })


if __name__ == "__main__":
    try:
        print("Node is starting...")
        app.run(debug=True, port=5004)
    except KeyboardInterrupt:
        print("\nNode is shutting down for restart...")
        time.sleep(1)
        print("Restarting node...")
        # Restart the script
        os.execl(sys.executable, sys.executable, *sys.argv)
