import unittest
from layer2_solutions.sharding.shard_manager import ShardManager # type: ignore
from blocks.blockchain_state import Blockchain

class TestCrossShardTransactions(unittest.TestCase):
    def setUp(self):
        """Set up shard manager and initialize two shards."""
        self.shard_manager = ShardManager()
        self.shard1 = self.shard_manager.create_shard("shard1")
        self.shard2 = self.shard_manager.create_shard("shard2")

        # Add initial balances
        self.shard1.blockchain.balances["Alice"] = 100
        self.shard2.blockchain.balances["Bob"] = 50

    def test_valid_cross_shard_transaction(self):
        """Tests a valid cross-shard transaction."""
        tx = {
            "sender": "Alice",
            "receiver": "Bob",
            "amount": 30,
            "from_shard": "shard1",
            "to_shard": "shard2"
        }

        # Process cross-shard transaction
        result = self.shard_manager.process_cross_shard_transaction(tx)
        self.assertTrue(result, "Valid cross-shard transaction was not processed")

        # Verify balances
        self.assertEqual(self.shard1.blockchain.get_balance("Alice"), 70, "Incorrect balance in shard1")
        self.assertEqual(self.shard2.blockchain.get_balance("Bob"), 80, "Incorrect balance in shard2")

    def test_invalid_cross_shard_transaction(self):
        """Tests an invalid cross-shard transaction (e.g., insufficient balance)."""
        tx = {
            "sender": "Alice",
            "receiver": "Bob",
            "amount": 150,  # Exceeds Alice's balance
            "from_shard": "shard1",
            "to_shard": "shard2"
        }

        # Process cross-shard transaction
        result = self.shard_manager.process_cross_shard_transaction(tx)
        self.assertFalse(result, "Invalid cross-shard transaction was incorrectly processed")

        # Verify balances remain unchanged
        self.assertEqual(self.shard1.blockchain.get_balance("Alice"), 100, "Balance in shard1 was incorrectly modified")
        self.assertEqual(self.shard2.blockchain.get_balance("Bob"), 50, "Balance in shard2 was incorrectly modified")

    def test_atomicity_of_cross_shard_transaction(self):
        """Tests that a cross-shard transaction is atomic (no partial updates)."""
        tx = {
            "sender": "Alice",
            "receiver": "Bob",
            "amount": 30,
            "from_shard": "shard1",
            "to_shard": "shard2"
        }

        # Simulate partial failure by forcing shard2 to reject the transaction
        self.shard_manager.simulate_failure("shard2")
        result = self.shard_manager.process_cross_shard_transaction(tx)
        self.assertFalse(result, "Cross-shard transaction was processed despite failure")

        # Verify atomicity: balances must remain unchanged
        self.assertEqual(self.shard1.blockchain.get_balance("Alice"), 100, "Atomicity violated in shard1")
        self.assertEqual(self.shard2.blockchain.get_balance("Bob"), 50, "Atomicity violated in shard2")

if __name__ == "__main__":
    unittest.main()
