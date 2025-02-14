import hashlib
import time
from blockchain.blocks.block import Block

class BlockBuilder:
    """Constructs new blocks by assembling transactions and metadata."""

    def __init__(self, difficulty=2):
        """
        Initializes the BlockBuilder.
        :param difficulty: The proof-of-work difficulty level.
        """
        self.difficulty = difficulty

    def create_block(self, index, previous_hash, transactions):
        """
        Creates a new block.
        :param index: The block's index in the chain.
        :param previous_hash: The hash of the previous block.
        :param transactions: A list of transactions to include in the block.
        :return: A new Block object.
        """
        timestamp = int(time.time())
        nonce = 0
        block = Block(index, previous_hash, timestamp, transactions, nonce, "")

        # Perform proof-of-work to find a valid nonce
        block.hash = self._mine_block(block)
        return block

    def _mine_block(self, block):
        """
        Mines a block by finding a nonce that satisfies the difficulty level.
        :param block: The block to mine.
        :return: The valid hash of the mined block.
        """
        while True:
            hash_value = self._compute_hash(block)
            if hash_value.startswith("0" * self.difficulty):
                return hash_value
            block.nonce += 1

    def _compute_hash(self, block):
        """
        Computes the hash of a block.
        :param block: The block to hash.
        :return: The SHA-256 hash of the block.
        """
        data = f"{block.index}{block.previous_hash}{block.timestamp}{block.transactions}{block.nonce}"
        return hashlib.sha256(data.encode()).hexdigest()


# Example Block class (replace with actual Block class)
class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, nonce, block_hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = block_hash


# Example usage
if __name__ == "__main__":
    # Example transactions
    transactions = [
        {"sender": "Alice", "receiver": "Bob", "amount": 50},
        {"sender": "Charlie", "receiver": "Dave", "amount": 20}
    ]

    # Previous block hash
    previous_hash = "0" * 64  # Simulated genesis block hash

    # Build a new block
    block_builder = BlockBuilder(difficulty=3)
    new_block = block_builder.create_block(index=1, previous_hash=previous_hash, transactions=transactions)

    # Print the block details
    print(f"Block Index: {new_block.index}")
    print(f"Previous Hash: {new_block.previous_hash}")
    print(f"Timestamp: {new_block.timestamp}")
    print(f"Transactions: {new_block.transactions}")
    print(f"Nonce: {new_block.nonce}")
    print(f"Hash: {new_block.hash}")
