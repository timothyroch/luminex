import hashlib
from blockchain.blocks.block import Block

class BlockValidation:
    """Validates blocks to ensure they adhere to the blockchain protocol rules."""

    def __init__(self, difficulty=2):
        """
        Initializes the BlockValidation class.
        :param difficulty: The difficulty level for proof-of-work validation.
        """
        self.difficulty = difficulty

    def validate_block_structure(self, block):
        """
        Validates the structure of a block.
        :param block: A Block object.
        :return: True if the structure is valid, False otherwise.
        """
        required_fields = ["index", "previous_hash", "timestamp", "transactions", "nonce", "hash"]
        for field in required_fields:
            if not hasattr(block, field):
                return False
        return True

    def validate_block_hash(self, block):
        """
        Validates the hash of a block to ensure it meets the difficulty requirement.
        :param block: A Block object.
        :return: True if the hash is valid, False otherwise.
        """
        computed_hash = block.compute_hash()
        if computed_hash != block.hash:
            return False
        return computed_hash.startswith("0" * self.difficulty)

    def validate_previous_hash(self, block, previous_block):
        """
        Ensures the block's previous hash matches the hash of the previous block.
        :param block: The current Block object.
        :param previous_block: The previous Block object.
        :return: True if the hashes match, False otherwise.
        """
        return block.previous_hash == previous_block.hash

    def validate_transactions(self, block, blockchain_state):
        """
        Validates all transactions in the block.
        :param block: A Block object.
        :param blockchain_state: The current state of the blockchain.
        :return: True if all transactions are valid, False otherwise.
        """
        for transaction in block.transactions:
            if not self.validate_transaction(transaction, blockchain_state):
                return False
        return True

    def validate_transaction(self, transaction, blockchain_state):
        """
        Validates a single transaction.
        :param transaction: A transaction dictionary.
        :param blockchain_state: The current state of the blockchain.
        :return: True if the transaction is valid, False otherwise.
        """
        sender = transaction["sender"]
        receiver = transaction["receiver"]
        amount = transaction["amount"]

        # Ensure sender has enough balance
        sender_balance = blockchain_state.get_balance(sender)
        if sender_balance < amount:
            return False

        # Additional checks (e.g., valid signatures) can be added here
        return True

    def validate_block(self, block, previous_block, blockchain_state):
        """
        Validates an entire block.
        :param block: A Block object.
        :param previous_block: The previous Block object.
        :param blockchain_state: The current state of the blockchain.
        :return: True if the block is valid, False otherwise.
        """
        if not self.validate_block_structure(block):
            return False

        if not self.validate_block_hash(block):
            return False

        if not self.validate_previous_hash(block, previous_block):
            return False

        if not self.validate_transactions(block, blockchain_state):
            return False

        return True


# Example usage
if __name__ == "__main__":
    # Simulated block and blockchain state for testing
    class MockBlockchainState:
        def __init__(self):
            self.balances = {"Alice": 100, "Bob": 50}

        def get_balance(self, user):
            return self.balances.get(user, 0)

    # Mock Block class
    class MockBlock:
        def __init__(self, index, previous_hash, transactions, nonce):
            self.index = index
            self.previous_hash = previous_hash
            self.timestamp = 1678912345
            self.transactions = transactions
            self.nonce = nonce
            self.hash = self.compute_hash()

        def compute_hash(self):
            data = f"{self.index}{self.previous_hash}{self.timestamp}{self.transactions}{self.nonce}"
            return hashlib.sha256(data.encode()).hexdigest()

    # Create a blockchain state
    blockchain_state = MockBlockchainState()

    # Create blocks for testing
    previous_block = MockBlock(0, "0", [], 0)
    block = MockBlock(1, previous_block.hash, [{"sender": "Alice", "receiver": "Bob", "amount": 20}], 12345)

    # Validate the block
    validator = BlockValidation(difficulty=2)
    is_valid = validator.validate_block(block, previous_block, blockchain_state)
    print("Block is valid:", is_valid)
