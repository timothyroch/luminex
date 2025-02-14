import unittest
from blocks.blockchain_state import Blockchain
from transactions.transaction_pool import TransactionPool
from blocks.block import Block

class TestDoubleSpending(unittest.TestCase):
    def setUp(self):
        """Set up a blockchain and transaction pool for testing."""
        self.blockchain = Blockchain()
        self.transaction_pool = TransactionPool()
        self.blockchain.create_genesis_block()

        # Add some initial balance to an account for testing
        self.initial_balance = 100
        self.sender = "Alice"
        self.receiver1 = "Bob"
        self.receiver2 = "Charlie"
        self.blockchain.balances[self.sender] = self.initial_balance

    def test_double_spending(self):
        """Tests that double-spending is detected and prevented."""
        # Create two conflicting transactions
        tx1 = {"sender": self.sender, "receiver": self.receiver1, "amount": 50}
        tx2 = {"sender": self.sender, "receiver": self.receiver2, "amount": 50}

        # Add the first transaction to the pool and mine a block
        self.transaction_pool.add_transaction(tx1, sender_balance=self.blockchain.get_balance(self.sender))
        pending_transactions = self.transaction_pool.get_pending_transactions(max_count=10)
        new_block = Block(self.blockchain.get_latest_block().index + 1, self.blockchain.get_latest_block().hash, pending_transactions)
        new_block.mine_block(difficulty=2)
        self.blockchain.add_block(new_block, difficulty=2)

        # Attempt to add the second (double-spend) transaction
        double_spend_attempt = self.transaction_pool.add_transaction(tx2, sender_balance=self.blockchain.get_balance(self.sender))

        # Assert that the double-spend attempt is rejected
        self.assertFalse(double_spend_attempt, "Double-spending transaction was incorrectly accepted.")

    def test_insufficient_balance(self):
        """Tests that transactions exceeding the sender's balance are rejected."""
        tx = {"sender": self.sender, "receiver": self.receiver1, "amount": 150}  # Exceeds balance
        result = self.transaction_pool.add_transaction(tx, sender_balance=self.blockchain.get_balance(self.sender))
        self.assertFalse(result, "Transaction with insufficient balance was incorrectly accepted.")

if __name__ == "__main__":
    unittest.main()
