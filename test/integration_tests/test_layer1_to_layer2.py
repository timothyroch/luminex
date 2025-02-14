import unittest
from layer2_solutions.zk_rollups.zk_rollup_manager import ZKRollupManager # type: ignore
from blocks.blockchain_state import Blockchain

class TestLayer1ToLayer2(unittest.TestCase):
    def setUp(self):
        """Set up the Layer 1 blockchain and Layer 2 zk-rollup system."""
        self.layer1 = Blockchain()
        self.zk_rollup = ZKRollupManager()

        # Add initial balances to Layer 1
        self.layer1.balances["Alice"] = 100
        self.layer1.balances["Bob"] = 50

    def test_deposit_to_layer2(self):
        """Tests depositing assets from Layer 1 to Layer 2."""
        deposit = {"sender": "Alice", "receiver": "Alice_L2", "amount": 40}
        result = self.zk_rollup.deposit(deposit, self.layer1)
        self.assertTrue(result, "Deposit to Layer 2 failed")

        # Verify Layer 1 and Layer 2 balances
        self.assertEqual(self.layer1.get_balance("Alice"), 60, "Incorrect balance on Layer 1 after deposit")
        self.assertEqual(self.zk_rollup.get_balance("Alice_L2"), 40, "Incorrect balance on Layer 2 after deposit")

    def test_withdraw_to_layer1(self):
        """Tests withdrawing assets from Layer 2 to Layer 1."""
        # Pre-deposit to Layer 2
        self.zk_rollup.balances["Bob_L2"] = 30

        withdrawal = {"sender": "Bob_L2", "receiver": "Bob", "amount": 30}
        result = self.zk_rollup.withdraw(withdrawal, self.layer1)
        self.assertTrue(result, "Withdrawal to Layer 1 failed")

        # Verify Layer 1 and Layer 2 balances
        self.assertEqual(self.layer1.get_balance("Bob"), 80, "Incorrect balance on Layer 1 after withdrawal")
        self.assertEqual(self.zk_rollup.get_balance("Bob_L2"), 0, "Incorrect balance on Layer 2 after withdrawal")

    def test_invalid_withdrawal(self):
        """Tests an invalid withdrawal (e.g., insufficient Layer 2 balance)."""
        withdrawal = {"sender": "Alice_L2", "receiver": "Alice", "amount": 100}  # Exceeds balance
        result = self.zk_rollup.withdraw(withdrawal, self.layer1)
        self.assertFalse(result, "Invalid withdrawal was incorrectly processed")

    def test_proof_verification(self):
        """Tests the validity of zk-proofs for Layer 2 withdrawals."""
        proof = self.zk_rollup.generate_proof({"sender": "Bob_L2", "amount": 30})
        is_valid = self.zk_rollup.verify_proof(proof)
        self.assertTrue(is_valid, "ZK-proof verification failed")

if __name__ == "__main__":
    unittest.main()
