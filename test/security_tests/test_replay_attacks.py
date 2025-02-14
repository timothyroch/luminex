import unittest
from blocks.blockchain_state import Blockchain
from transactions.transaction_pool import TransactionPool
from blocks.block import Block

class TestReplayAttacks(unittest.TestCase):
    def setUp(self):
        """Set up a blockchain and transaction pool for testing."""
        self.blockchain = Blockchain()
        self.transaction_pool = TransactionPool()
        self.blockchain.create_genesis_block()

        # Add initial balance for testing
        self.sender = "Alice"
        self.receiver = "Bob"
        self.blockchain.balances[self.sender] = 100

        # Create a valid transaction
        self.valid_transaction = {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": 50
        }
        self.transaction_hash = self.hash_transaction(self.valid_transaction)

    def hash_transaction(self, transaction):
        """Generates a hash for a transaction."""
        import hashlib
        tx_string = f"{transaction['sender']}{transaction['receiver']}{transaction['amount']}"
        return hashlib.sha256(tx_string.encode()).hexdigest()

    def test_replay_attack(self):
        """Tests that replaying a transaction is detected and rejected."""
        # Add the valid transaction to the pool and mine it
        self.transaction_pool.add_transaction(self.valid_transaction, sender_balance=self.blockchain.get_balance(self.sender))
        pending_transactions = self.transaction_pool.get_pending_transactions(max_count=10)
        new_block = Block(self.blockchain.get_latest_block().index + 1, self.blockchain.get_latest_block().hash, pending_transactions)
        new_block.mine_block(difficulty=2)
        self.blockchain.add_block(new_block, difficulty=2)

        # Attempt to replay the same transaction
        replay_attempt = self.transaction_pool.add_transaction(self.valid_transaction, sender_balance=self.blockchain.get_balance(self.sender))

        # Assert that the replay attempt is rejected
        self.assertFalse(replay_attempt, "Replay attack transaction was incorrectly accepted.")

    def test_unique_transaction_hashes(self):
        """Ensures transaction hashes are unique and prevent duplication."""
        tx1 = {"sender": "Alice", "receiver": "Bob", "amount": 10}
        tx2 = {"sender": "Alice", "receiver": "Bob", "amount": 10}  # Identical to tx1
        hash1 = self.hash_transaction(tx1)
        hash2 = self.hash_transaction(tx2)

        # Ensure the hashes are the same, indicating identical transactions
        self.assertEqual(hash1, hash2, "Identical transactions produced different hashes.")

        # Add tx1 to the pool
        self.transaction_pool.add_transaction(tx1, sender_balance=self.blockchain.get_balance(self.sender))

        # Attempt to add tx2 (should be rejected due to duplication)
        result = self.transaction_pool.add_transaction(tx2, sender_balance=self.blockchain.get_balance(self.sender))
        self.assertFalse(result, "Duplicate transaction was incorrectly accepted.")

if __name__ == "__main__":
    unittest.main()
