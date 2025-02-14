import unittest
from cryptocurrency.wallet.key_management.key_generator import KeyGenerator
from cryptocurrency.wallet.key_management.key_signer import KeySigner
from cryptocurrency.wallet.balance_tracker import BalanceTracker
from cryptocurrency.wallet.multisig import MultiSigWallet
from blockchain.transactions.transaction import Transaction

class TestWallet(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing wallet operations.
        """
        self.key_generator = KeyGenerator()
        self.key_signer = KeySigner()
        self.balance_tracker = BalanceTracker()
        self.multisig_wallet = MultiSigWallet(signers=["key1", "key2", "key3"], required_signatures=2)

        # Generate keys for testing
        self.private_key, self.public_key = self.key_generator.generate_key_pair()

        # Sample transaction
        self.transaction = Transaction(
            sender="address1",
            recipient="address2",
            amount=50,
            timestamp=1673367600,
            signature=""
        )

    def test_key_generation(self):
        """
        Test that the key generator produces a valid key pair.
        """
        private_key, public_key = self.key_generator.generate_key_pair()
        self.assertIsNotNone(private_key, "Private key generation failed")
        self.assertIsNotNone(public_key, "Public key generation failed")
        print("Key generation test passed.")

    def test_sign_transaction(self):
        """
        Test that a transaction can be signed with the private key.
        """
        signature = self.key_signer.sign_transaction(self.transaction, self.private_key)
        self.transaction.signature = signature
        self.assertTrue(self.key_signer.verify_signature(self.transaction, self.public_key), "Transaction signature verification failed")
        print("Transaction signing test passed.")

    def test_balance_tracking(self):
        """
        Test that the balance tracker accurately updates and retrieves balances.
        """
        self.balance_tracker.update_balance("address1", -50)
        self.balance_tracker.update_balance("address2", 50)
        balance1 = self.balance_tracker.get_balance("address1")
        balance2 = self.balance_tracker.get_balance("address2")
        self.assertEqual(balance1, -50, "Balance tracking for sender is incorrect")
        self.assertEqual(balance2, 50, "Balance tracking for recipient is incorrect")
        print("Balance tracking test passed.")

    def test_multisig_transaction(self):
        """
        Test that a multisig wallet requires the correct number of signatures for a transaction.
        """
        signatures = [
            self.key_signer.sign_message("Sample Data", "key1"),
            self.key_signer.sign_message("Sample Data", "key2")
        ]
        is_valid = self.multisig_wallet.verify_signatures("Sample Data", signatures)
        self.assertTrue(is_valid, "Multisig verification failed with valid signatures")
        print("Multisig transaction test passed.")

    def test_insufficient_multisig_signatures(self):
        """
        Test that a multisig wallet rejects insufficient signatures.
        """
        signatures = [
            self.key_signer.sign_message("Sample Data", "key1")
        ]
        is_valid = self.multisig_wallet.verify_signatures("Sample Data", signatures)
        self.assertFalse(is_valid, "Multisig verification passed with insufficient signatures")
        print("Insufficient multisig signatures test passed.")

if __name__ == "__main__":
    unittest.main()
