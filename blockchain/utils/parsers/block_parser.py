import json
from hashlib import sha256
from utils.merkle_tree import MerkleTree  # type: ignore # Assuming MerkleTree is implemented in utils/merkle_tree.py
from utils.data_serializer import DataSerializer  # Assuming DataSerializer is in utils/

class BlockParser:
    """Parses and validates raw block data."""

    def __init__(self):
        pass

    @staticmethod
    def parse_raw_block(raw_block):
        """
        Parses raw block data into a structured dictionary.
        :param raw_block: The raw block data (JSON or binary format).
        :return: A structured block dictionary.
        """
        try:
            if isinstance(raw_block, bytes):
                block_data = DataSerializer.deserialize_from_binary(raw_block)
            elif isinstance(raw_block, str):
                block_data = json.loads(raw_block)
            else:
                raise ValueError("Unsupported block data format.")
            return block_data
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Failed to parse block: {e}")

    @staticmethod
    def validate_block_structure(block):
        """
        Validates the structure of a block.
        :param block: The block data as a dictionary.
        :return: True if the structure is valid, raises ValueError otherwise.
        """
        required_fields = ["index", "timestamp", "transactions", "previous_hash", "nonce", "merkle_root"]
        for field in required_fields:
            if field not in block:
                raise ValueError(f"Missing required block field: {field}")
        if not isinstance(block["transactions"], list):
            raise ValueError("Transactions must be a list.")
        return True

    @staticmethod
    def recompute_merkle_root(transactions):
        """
        Recomputes the Merkle root from the transactions.
        :param transactions: A list of transaction data.
        :return: The recomputed Merkle root as a hexadecimal string.
        """
        transaction_hashes = [sha256(json.dumps(tx).encode('utf-8')).hexdigest() for tx in transactions]
        merkle_tree = MerkleTree(transaction_hashes)
        return merkle_tree.root

    @staticmethod
    def validate_merkle_root(block):
        """
        Validates the Merkle root in the block.
        :param block: The block data as a dictionary.
        :return: True if the Merkle root is valid, raises ValueError otherwise.
        """
        recomputed_root = BlockParser.recompute_merkle_root(block["transactions"])
        if recomputed_root != block["merkle_root"]:
            raise ValueError("Invalid Merkle root.")
        return True

    @staticmethod
    def validate_block(block):
        """
        Fully validates a block by checking its structure, Merkle root, and other components.
        :param block: The block data as a dictionary.
        :return: True if the block is valid, raises ValueError otherwise.
        """
        BlockParser.validate_block_structure(block)
        BlockParser.validate_merkle_root(block)
        # Add additional block validation logic here (e.g., proof of work or proof of stake validation)
        return True


# Example usage
if __name__ == "__main__":
    # Example raw block (in JSON format)
    raw_block = """
    {
        "index": 1,
        "timestamp": "2025-01-10T16:00:00",
        "transactions": [
            {"sender": "Alice", "receiver": "Bob", "amount": 50},
            {"sender": "Charlie", "receiver": "Dave", "amount": 30}
        ],
        "previous_hash": "0xabcdef",
        "nonce": 12345,
        "merkle_root": "0xexamplemerkle"
    }
    """

    try:
        parser = BlockParser()
        block = parser.parse_raw_block(raw_block)
        print("Parsed Block:", block)

        # Validate block
        if parser.validate_block(block):
            print("Block is valid.")
    except ValueError as e:
        print("Block validation failed:", e)
