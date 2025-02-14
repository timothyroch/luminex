import json
from hashlib import sha256
from blockchain.transactions.transaction import Transaction
from blockchain.blocks.block import Block

class TestHelpers:
    @staticmethod
    def hash_data(data):
        """
        Generate a SHA-256 hash for the given data.
        """
        if isinstance(data, (dict, list)):
            data = json.dumps(data, sort_keys=True)
        return sha256(data.encode()).hexdigest()

    @staticmethod
    def validate_transaction_structure(transaction):
        """
        Validate the structure of a transaction object.
        """
        required_fields = ["sender", "recipient", "amount", "timestamp", "signature"]
        for field in required_fields:
            if not hasattr(transaction, field):
                raise ValueError(f"Transaction is missing required field: {field}")
        return True

    @staticmethod
    def validate_block_structure(block):
        """
        Validate the structure of a block object.
        """
        required_fields = ["index", "previous_hash", "data", "timestamp", "nonce", "hash"]
        for field in required_fields:
            if not hasattr(block, field):
                raise ValueError(f"Block is missing required field: {field}")
        return True

    @staticmethod
    def compare_blockchain_states(state1, state2):
        """
        Compare two blockchain states for equality.
        """
        return json.dumps(state1, sort_keys=True) == json.dumps(state2, sort_keys=True)

    @staticmethod
    def generate_mock_transaction(sender, recipient, amount):
        """
        Generate a mock transaction for testing purposes.
        """
        return Transaction(
            sender=sender,
            recipient=recipient,
            amount=amount,
            timestamp=1673367600,
            signature="MOCK_SIGNATURE"
        )

    @staticmethod
    def generate_mock_block(previous_hash, num_transactions=5):
        """
        Generate a mock block with random transactions.
        """
        transactions = [
            TestHelpers.generate_mock_transaction(f"address{i}", f"address{i+1}", i * 10)
            for i in range(1, num_transactions + 1)
        ]
        block_data = "".join(tx.sender for tx in transactions)
        block_hash = sha256(block_data.encode()).hexdigest()
        return Block(
            index=1,
            previous_hash=previous_hash,
            data=transactions,
            timestamp=1673368600,
            nonce=12345,
            hash=block_hash
        )

    @staticmethod
    def log_test_result(test_name, result):
        """
        Log the result of a test case.
        """
        status = "PASSED" if result else "FAILED"
        print(f"Test '{test_name}': {status}")

if __name__ == "__main__":
    # Example usage of TestHelpers
    try:
        mock_transaction = TestHelpers.generate_mock_transaction("address1", "address2", 50)
        TestHelpers.validate_transaction_structure(mock_transaction)
        print("Mock transaction validation: PASSED")

        mock_block = TestHelpers.generate_mock_block("0" * 64)
        TestHelpers.validate_block_structure(mock_block)
        print("Mock block validation: PASSED")

        state1 = {"address1": 100, "address2": 50}
        state2 = {"address1": 100, "address2": 50}
        is_equal = TestHelpers.compare_blockchain_states(state1, state2)
        print(f"Blockchain state comparison: {'PASSED' if is_equal else 'FAILED'}")

    except ValueError as e:
        print(f"Error: {e}")
