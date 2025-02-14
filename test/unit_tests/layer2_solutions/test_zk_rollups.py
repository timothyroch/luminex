import unittest
from layer2_solutions.zk_rollups.zk_rollup_engine import ZKRollupEngine
from layer2_solutions.zk_rollups.zk_proof_generator import ZKProofGenerator
from layer2_solutions.zk_rollups.rollup_verifier import RollupVerifier
from blockchain.transactions.transaction import Transaction

class TestZKRollups(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing ZK Rollups.
        """
        self.zk_rollup_engine = ZKRollupEngine(batch_size=5)
        self.zk_proof_generator = ZKProofGenerator()
        self.rollup_verifier = RollupVerifier()

        # Sample transactions for rollups
        self.transactions = [
            Transaction(sender=f"address{i}", recipient=f"address{i+1}", amount=10 * i, timestamp=1673367600 + i, signature=f"sig{i}")
            for i in range(1, 6)
        ]

    def test_batch_aggregation(self):
        """
        Test that the ZK Rollup engine correctly aggregates transactions into a batch.
        """
        batch = self.zk_rollup_engine.aggregate_transactions(self.transactions)
        self.assertEqual(len(batch), 5, "Batch size does not match expected transaction count")
        print("Batch aggregation test passed.")

    def test_proof_generation(self):
        """
        Test that a zero-knowledge proof is successfully generated for a batch of transactions.
        """
        batch = self.zk_rollup_engine.aggregate_transactions(self.transactions)
        zk_proof = self.zk_proof_generator.generate_proof(batch)
        self.assertIsNotNone(zk_proof, "Failed to generate zero-knowledge proof")
        print("Proof generation test passed.")

    def test_rollup_verification(self):
        """
        Test that a valid zero-knowledge proof for a rollup batch is successfully verified.
        """
        batch = self.zk_rollup_engine.aggregate_transactions(self.transactions)
        zk_proof = self.zk_proof_generator.generate_proof(batch)
        is_verified = self.rollup_verifier.verify_proof(batch, zk_proof)
        self.assertTrue(is_verified, "Zero-knowledge proof verification failed")
        print("Rollup verification test passed.")

    def test_invalid_proof_rejection(self):
        """
        Test that an invalid zero-knowledge proof is rejected during verification.
        """
        batch = self.zk_rollup_engine.aggregate_transactions(self.transactions)
        invalid_proof = "INVALID_PROOF"
        is_verified = self.rollup_verifier.verify_proof(batch, invalid_proof)
        self.assertFalse(is_verified, "Invalid zero-knowledge proof was incorrectly verified")
        print("Invalid proof rejection test passed.")

    def test_batch_size_limit(self):
        """
        Test that the ZK Rollup engine enforces the batch size limit.
        """
        large_batch = self.transactions + [
            Transaction(sender="extra", recipient="extra_recipient", amount=100, timestamp=1673367650, signature="extra_sig")
        ]
        with self.assertRaises(ValueError):
            self.zk_rollup_engine.aggregate_transactions(large_batch)
        print("Batch size limit test passed.")

if __name__ == "__main__":
    unittest.main()
