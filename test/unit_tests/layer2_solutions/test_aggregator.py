import unittest
from layer2_solutions.aggregator.transaction_router import TransactionRouter
from layer2_solutions.aggregator.state_syncer import StateSyncer
from layer2_solutions.aggregator.batch_processor import BatchProcessor
from blockchain.transactions.transaction import Transaction

class TestAggregator(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing the aggregator module.
        """
        self.transaction_router = TransactionRouter()
        self.state_syncer = StateSyncer()
        self.batch_processor = BatchProcessor(batch_size=3)

        # Sample transactions
        self.transactions = [
            Transaction(sender=f"address{i}", recipient=f"address{i+1}", amount=10 * i, timestamp=1673367600 + i, signature=f"sig{i}")
            for i in range(1, 6)
        ]

    def test_route_transaction_to_layer2(self):
        """
        Test that transactions are correctly routed to the appropriate Layer 2 solution.
        """
        layer2_target = self.transaction_router.route_transaction(self.transactions[0])
        self.assertIn(layer2_target, ["zk_rollup", "sidechain", "state_channel"], "Transaction routing failed")
        print("Transaction routing test passed.")

    def test_state_synchronization(self):
        """
        Test that the state syncer correctly synchronizes the state between Layer 1 and Layer 2.
        """
        sync_status = self.state_syncer.sync_state(layer2_id="zk_rollup", state_data={"balances": {"address1": 100}})
        self.assertTrue(sync_status, "State synchronization failed")
        print("State synchronization test passed.")

    def test_batch_processing(self):
        """
        Test that transactions are correctly batched by the batch processor.
        """
        batch = self.batch_processor.process_batch(self.transactions[:3])
        self.assertEqual(len(batch), 3, "Batch processing did not return the expected number of transactions")
        print("Batch processing test passed.")

    def test_batch_size_limit(self):
        """
        Test that the batch processor enforces the batch size limit.
        """
        with self.assertRaises(ValueError):
            self.batch_processor.process_batch(self.transactions[:5])
        print("Batch size limit test passed.")

    def test_proof_submission(self):
        """
        Test that proofs generated for Layer 2 batches are submitted correctly to Layer 1.
        """
        proof = self.batch_processor.generate_proof(self.transactions[:3])
        submission_status = self.batch_processor.submit_proof_to_layer1(proof)
        self.assertTrue(submission_status, "Proof submission to Layer 1 failed")
        print("Proof submission test passed.")

if __name__ == "__main__":
    unittest.main()
