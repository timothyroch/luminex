import unittest
from unittest.mock import patch, MagicMock
from api.transaction_api.endpoints.create_transaction import create_transaction
from api.transaction_api.endpoints.broadcast_transaction import broadcast_transaction
from api.transaction_api.endpoints.validate_transaction import validate_transaction
from blockchain.transactions.transaction import Transaction

class TestTransactionAPI(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing the transaction API.
        """
        self.transaction_data = {
            "sender": "address1",
            "recipient": "address2",
            "amount": 50,
            "timestamp": 1673367600,
            "signature": "VALID_SIGNATURE"
        }
        self.transaction = Transaction(**self.transaction_data)

    @patch("api.transaction_api.endpoints.create_transaction.Transaction")
    def test_create_transaction(self, mock_transaction):
        """
        Test the create transaction endpoint.
        """
        mock_transaction.return_value = self.transaction
        response = create_transaction(self.transaction_data)
        self.assertEqual(response["status"], "success", "Failed to create transaction")
        self.assertEqual(response["data"]["sender"], "address1", "Sender mismatch in created transaction")
        print("Create transaction test passed.")

    @patch("api.transaction_api.endpoints.broadcast_transaction.broadcast_to_peers")
    def test_broadcast_transaction(self, mock_broadcast):
        """
        Test the broadcast transaction endpoint.
        """
        mock_broadcast.return_value = True
        response = broadcast_transaction(self.transaction)
        self.assertEqual(response["status"], "success", "Failed to broadcast transaction")
        print("Broadcast transaction test passed.")

    @patch("api.transaction_api.endpoints.validate_transaction.TransactionValidator")
    def test_validate_transaction(self, mock_validator):
        """
        Test the validate transaction endpoint.
        """
        mock_validator().validate_transaction.return_value = True
        response = validate_transaction(self.transaction)
        self.assertEqual(response["status"], "success", "Failed to validate transaction")
        self.assertTrue(response["data"]["is_valid"], "Transaction validation failed")
        print("Validate transaction test passed.")

    @patch("api.transaction_api.endpoints.validate_transaction.TransactionValidator")
    def test_invalid_transaction(self, mock_validator):
        """
        Test validation of an invalid transaction.
        """
        mock_validator().validate_transaction.return_value = False
        response = validate_transaction(self.transaction)
        self.assertEqual(response["status"], "error", "Invalid transaction was not detected")
        print("Invalid transaction test passed.")

if __name__ == "__main__":
    unittest.main()
