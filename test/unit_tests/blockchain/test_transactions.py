import unittest
from blockchain.transactions.transaction import Transaction
from blockchain.transactions.transaction_validation import TransactionValidator
from blockchain.transactions.transaction_pool import TransactionPool

class TestTransactions(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing transactions.
        """
        self.valid_transaction = Transaction(
            sender="address1",
            recipient="address2",
            amount=100,
            timestamp=1673367600,
            signature="VALID_SIGNATURE"
        )
        self.invalid_transaction = Transaction(
            sender="address1",
            recipient="address2",
            amount=-50,  # Invalid amount
            timestamp=1673367600,
            signature="INVALID_SIGNATURE"
        )
        self.transaction_validator = TransactionValidator()
        self.transaction_pool = TransactionPool()

    def test_transaction_creation(self):
        """
        Test the creation of a transaction and its basic structure.
        """
        self.assertEqual(self.valid_transaction.sender, "address1", "Transaction sender mismatch")
        self.assertEqual(self.valid_transaction.recipient, "address2", "Transaction recipient mismatch")
        self.assertEqual(self.valid_transaction.amount, 100, "Transaction amount mismatch")
        print("Transaction creation test passed.")

    def test_valid_transaction(self):
        """
        Test that a valid transaction passes validation.
        """
        is_valid = self.transaction_validator.validate_transaction(self.valid_transaction)
        self.assertTrue(is_valid, "Valid transaction failed validation")
        print("Valid transaction test passed.")

    def test_invalid_transaction(self):
        """
        Test that an invalid transaction is rejected.
        """
        is_valid = self.transaction_validator.validate_transaction(self.invalid_transaction)
        self.assertFalse(is_valid, "Invalid transaction passed validation")
        print("Invalid transaction test passed.")

    def test_add_transaction_to_pool(self):
        """
        Test adding a valid transaction to the transaction pool.
        """
        self.transaction_pool.add_transaction(self.valid_transaction)
        self.assertIn(self.valid_transaction, self.transaction_pool.get_transactions(), "Transaction not added to pool")
        print("Transaction pool add test passed.")

    def test_reject_invalid_transaction_in_pool(self):
        """
        Test that an invalid transaction is not added to the transaction pool.
        """
        with self.assertRaises(ValueError):
            self.transaction_pool.add_transaction(self.invalid_transaction)
        print("Transaction pool rejection test passed.")

    def test_transaction_pool_size(self):
        """
        Test the size of the transaction pool after adding transactions.
        """
        self.transaction_pool.add_transaction(self.valid_transaction)
        self.assertEqual(len(self.transaction_pool.get_transactions()), 1, "Transaction pool size mismatch")
        print("Transaction pool size test passed.")

    def test_remove_transaction_from_pool(self):
        """
        Test removing a transaction from the transaction pool.
        """
        self.transaction_pool.add_transaction(self.valid_transaction)
        self.transaction_pool.remove_transaction(self.valid_transaction)
        self.assertNotIn(self.valid_transaction, self.transaction_pool.get_transactions(), "Transaction not removed from pool")
        print("Transaction pool remove test passed.")

if __name__ == "__main__":
    unittest.main()
