import json

class BlockFinalization:
    """Handles the process of block finalization and confirmation based on consensus rules."""

    def __init__(self, config_file="blockchain/consensus/consensus_config.json"):
        """
        Initializes the BlockFinalization class by loading configuration.
        :param config_file: Path to the JSON configuration file.
        """
        with open(config_file) as file:
            self.config = json.load(file)
        self.finalization_threshold = self.config["finalization_threshold"]

    def finalize_block(self, block, votes):
        """
        Finalizes a block if the number of unique validator votes meets the finalization threshold.
        :param block: A dictionary representing the block to be finalized.
        :param votes: A list of validator IDs who voted for the block.
        :return: True if the block is finalized, False otherwise.
        """
        unique_votes = set(votes)
        total_validators = len(unique_votes)
        threshold = int(len(votes) * self.finalization_threshold)

        if total_validators >= threshold:
            block["finalized"] = True
            return True
        return False

    def validate_block(self, block):
        """
        Validates the block structure and contents before finalization.
        :param block: A dictionary representing the block.
        :return: True if the block is valid, False otherwise.
        """
        required_fields = ["index", "previous_hash", "hash", "transactions", "timestamp"]
        for field in required_fields:
            if field not in block:
                return False
        return True

    def log_finalization_event(self, block, status):
        """
        Logs block finalization events for monitoring and auditing.
        :param block: The finalized block.
        :param status: Finalization status (e.g., 'success', 'failure').
        """
        with open("monitoring/logs/block_finalization.log", "a") as log_file:
            log_file.write(f"Block {block['index']} - Finalization {status}\n")


# Example usage
if __name__ == "__main__":
    # Sample block and votes
    block = {
        "index": 5,
        "previous_hash": "abc123",
        "hash": "def456",
        "transactions": [{"sender": "Alice", "receiver": "Bob", "amount": 50}],
        "timestamp": 1678912345,
        "finalized": False
    }
    votes = ["Validator1", "Validator2", "Validator3"]

    finalizer = BlockFinalization()

    # Validate block before finalization
    if finalizer.validate_block(block):
        print(f"Block {block['index']} is valid.")
        finalized = finalizer.finalize_block(block, votes)
        status = "success" if finalized else "failure"
        print(f"Block Finalized: {finalized}")
        finalizer.log_finalization_event(block, status)
    else:
        print(f"Block {block['index']} is invalid.")
