import os
import json
import subprocess
from pathlib import Path

class TestnetSetup:
    def __init__(self, config_file="testnet_config.json"):
        """
        Initialize the testnet setup using the provided configuration file.
        """
        self.config_file = config_file
        self.config = self.load_config()
        self.nodes_dir = Path(self.config["nodes_directory"])
        self.genesis_file = Path(self.config["genesis_file"])

    def load_config(self):
        """
        Load the testnet configuration from the JSON file.
        """
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file '{self.config_file}' not found.")
        with open(self.config_file, "r") as file:
            return json.load(file)

    def create_directories(self):
        """
        Create directories for testnet nodes.
        """
        if not self.nodes_dir.exists():
            self.nodes_dir.mkdir(parents=True)
        for i in range(self.config["number_of_nodes"]):
            node_path = self.nodes_dir / f"node_{i+1}"
            node_path.mkdir(exist_ok=True)
            print(f"Created directory for node {i+1}: {node_path}")

    def generate_genesis_block(self):
        """
        Generate the genesis block for the testnet.
        """
        print("Generating genesis block...")
        genesis_data = {
            "chain_id": self.config["chain_id"],
            "alloc": self.config["initial_allocations"],
            "timestamp": self.config["genesis_timestamp"],
            "difficulty": self.config["genesis_difficulty"],
            "nonce": self.config["genesis_nonce"],
        }
        with open(self.genesis_file, "w") as file:
            json.dump(genesis_data, file, indent=4)
        print(f"Genesis block generated at: {self.genesis_file}")

    def initialize_nodes(self):
        """
        Initialize each testnet node with the genesis block.
        """
        for i in range(self.config["number_of_nodes"]):
            node_path = self.nodes_dir / f"node_{i+1}"
            genesis_dest = node_path / "genesis.json"
            subprocess.run(["cp", str(self.genesis_file), str(genesis_dest)], check=True)
            print(f"Initialized node {i+1} with genesis block.")

    def start_testnet(self):
        """
        Start all testnet nodes.
        """
        for i in range(self.config["number_of_nodes"]):
            node_path = self.nodes_dir / f"node_{i+1}"
            command = [
                "blockchain_node",  # Replace with actual node executable
                "--datadir", str(node_path),
                "--genesis", str(node_path / "genesis.json"),
                "--port", str(self.config["base_port"] + i),
                "--network_id", str(self.config["chain_id"]),
            ]
            print(f"Starting node {i+1} with command: {' '.join(command)}")
            subprocess.Popen(command)
        print("All testnet nodes started.")

    def run(self):
        """
        Execute the testnet setup process.
        """
        self.create_directories()
        self.generate_genesis_block()
        self.initialize_nodes()
        self.start_testnet()
        print("Testnet setup complete.")

if __name__ == "__main__":
    setup = TestnetSetup()
    setup.run()
