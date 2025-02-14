import json
import yaml # type: ignore
import os

class ConfigLoader:
    """Loads and parses configuration files for the blockchain system."""

    def __init__(self, config_dir="config", default_config="config.json"):
        """
        Initializes the ConfigLoader with the specified configuration directory and default file.
        :param config_dir: The directory containing configuration files.
        :param default_config: The default configuration file to load if none is specified.
        """
        self.config_dir = config_dir
        self.default_config = default_config
        os.makedirs(self.config_dir, exist_ok=True)  # Ensure config directory exists

    def load_config(self, file_name=None):
        """
        Loads a configuration file (JSON or YAML).
        :param file_name: The name of the configuration file (default: default_config).
        :return: The parsed configuration as a dictionary.
        """
        file_name = file_name or self.default_config
        file_path = os.path.join(self.config_dir, file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Configuration file '{file_path}' not found.")

        with open(file_path, "r") as file:
            if file_name.endswith(".json"):
                return json.load(file)
            elif file_name.endswith(".yaml") or file_name.endswith(".yml"):
                return yaml.safe_load(file)
            else:
                raise ValueError("Unsupported configuration file format. Use JSON or YAML.")

    def save_config(self, config_data, file_name=None):
        """
        Saves a configuration to a file.
        :param config_data: The configuration data as a dictionary.
        :param file_name: The name of the configuration file (default: default_config).
        """
        file_name = file_name or self.default_config
        file_path = os.path.join(self.config_dir, file_name)

        with open(file_path, "w") as file:
            if file_name.endswith(".json"):
                json.dump(config_data, file, indent=4)
            elif file_name.endswith(".yaml") or file_name.endswith(".yml"):
                yaml.dump(config_data, file, default_flow_style=False)
            else:
                raise ValueError("Unsupported configuration file format. Use JSON or YAML.")

        print(f"Configuration saved to '{file_path}'.")

    def get_value(self, config_data, key_path):
        """
        Retrieves a nested value from the configuration data using a key path.
        :param config_data: The configuration data as a dictionary.
        :param key_path: The key path (e.g., "network.port").
        :return: The value associated with the key path, or None if not found.
        """
        keys = key_path.split(".")
        value = config_data
        for key in keys:
            if key in value:
                value = value[key]
            else:
                return None
        return value

    def set_value(self, config_data, key_path, value):
        """
        Sets a nested value in the configuration data using a key path.
        :param config_data: The configuration data as a dictionary.
        :param key_path: The key path (e.g., "network.port").
        :param value: The value to set.
        """
        keys = key_path.split(".")
        d = config_data
        for key in keys[:-1]:
            if key not in d:
                d[key] = {}
            d = d[key]
        d[keys[-1]] = value


# Example usage
if __name__ == "__main__":
    config_loader = ConfigLoader()

    # Example default configuration data
    default_config = {
        "network": {
            "host": "127.0.0.1",
            "port": 8080
        },
        "blockchain": {
            "consensus": "PoS",
            "block_time": 10
        },
        "logging": {
            "level": "INFO",
            "log_dir": "logs"
        }
    }

    # Save default configuration
    config_loader.save_config(default_config, "config.json")

    # Load configuration
    config = config_loader.load_config("config.json")
    print("Loaded Configuration:", config)

    # Get a nested value
    port = config_loader.get_value(config, "network.port")
    print("Network Port:", port)

    # Set a nested value
    config_loader.set_value(config, "network.port", 9090)
    print("Updated Configuration:", config)

    # Save updated configuration
    config_loader.save_config(config, "config.json")
