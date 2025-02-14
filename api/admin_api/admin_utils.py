import json
import logging
import os
from typing import Dict, Any, Optional

# Configure logging for administrative tasks
logging.basicConfig(
    filename="logs/admin_utils.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def log_message(level: str, message: str) -> None:
    """
    Logs a message to the admin utilities log file.
    :param level: The logging level (INFO, WARNING, ERROR, etc.).
    :param message: The message to log.
    """
    log_function = getattr(logging, level.lower(), None)
    if callable(log_function):
        log_function(message)
    else:
        logging.error(f"Invalid logging level: {level}. Message: {message}")


def load_config(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Loads a JSON configuration file.
    :param file_path: Path to the configuration file.
    :return: Dictionary containing the configuration data, or None if an error occurs.
    """
    if not os.path.exists(file_path):
        log_message("error", f"Configuration file not found: {file_path}")
        return None

    try:
        with open(file_path, "r") as file:
            config = json.load(file)
            log_message("info", f"Configuration loaded successfully from {file_path}")
            return config
    except json.JSONDecodeError as e:
        log_message("error", f"Error decoding JSON from {file_path}: {e}")
    except Exception as e:
        log_message("error", f"Unexpected error loading config from {file_path}: {e}")
    return None


def validate_node_url(node_url: str) -> bool:
    """
    Validates a node URL format.
    :param node_url: The node URL to validate.
    :return: True if valid, False otherwise.
    """
    if node_url.startswith("http://") or node_url.startswith("https://"):
        log_message("info", f"Valid node URL: {node_url}")
        return True
    else:
        log_message("warning", f"Invalid node URL: {node_url}")
        return False


def sanitize_input(input_data: str) -> str:
    """
    Sanitizes input data to prevent injection attacks or invalid characters.
    :param input_data: The input string to sanitize.
    :return: Sanitized input string.
    """
    sanitized = input_data.strip().replace("'", "").replace("\"", "")
    log_message("info", f"Input sanitized: {sanitized}")
    return sanitized


def calculate_uptime(start_time: float) -> str:
    """
    Calculates the uptime of the node in a human-readable format.
    :param start_time: The start time of the node in seconds since epoch.
    :return: Uptime as a human-readable string (e.g., "1d 2h 30m").
    """
    import time
    elapsed_seconds = int(time.time() - start_time)
    days, seconds = divmod(elapsed_seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    uptime = f"{days}d {hours}h {minutes}m" if days > 0 else f"{hours}h {minutes}m"
    log_message("info", f"Uptime calculated: {uptime}")
    return uptime


# Example usage
if __name__ == "__main__":
    log_message("info", "Admin utilities module started.")

    # Load configuration
    config = load_config("admin_config.json")
    print("Loaded Config:", config)

    # Validate node URL
    is_valid = validate_node_url("http://node1.blockchain.net")
    print("Is Node URL Valid?", is_valid)

    # Sanitize input
    sanitized_input = sanitize_input(" malicious'input\" ")
    print("Sanitized Input:", sanitized_input)

    # Calculate uptime
    start_time = 1673445600  # Example start time
    uptime = calculate_uptime(start_time)
    print("Uptime:", uptime)
