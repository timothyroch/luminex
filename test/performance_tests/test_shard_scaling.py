import unittest
import time
from layer2_solutions.sharding.shard_manager import ShardManager # type: ignore
from transactions.transaction_pool import TransactionPool

class TestShardScaling(unittest.TestCase):
    def setUp(self):
        """Set up a shard manager and initial shards."""
        self.shard_manager = ShardManager()
        self.transaction_pool = TransactionPool()
        self.initial_shards = 2  # Start with 2 shards
        for i in range(self.initial_shards):
            self.shard_manager.create_shard(f"shard{i+1}")

    def generate_transactions(self, num_transactions, shard_count):
        """Generates random transactions distributed across shards."""
        transactions = []
        for i in range(num_transactions):
            sender_shard = f"shard{(i % shard_count) + 1}"
            receiver_shard = f"shard{((i + 1) % shard_count) + 1}"
            transactions.append({
                "sender": f"User{i}@{sender_shard}",
                "receiver": f"User{i+1}@{receiver_shard}",
                "amount": 10
            })
        return transactions

    def test_scaling_performance(self):
        """Tests performance as the number of shards increases."""
        num_transactions = 1000
        shard_counts = [2, 4, 8, 16]  # Test with different shard counts
        results = []

        for shard_count in shard_counts:
            # Create the necessary number of shards
            self.shard_manager.clear_shards()
            for i in range(shard_count):
                self.shard_manager.create_shard(f"shard{i+1}")

            # Generate and add transactions to the pool
            transactions = self.generate_transactions(num_transactions, shard_count)
            for tx in transactions:
                self.transaction_pool.add_transaction(tx, sender_balance=1000)

            # Measure transaction processing time
            start_time = time.time()
            self.shard_manager.process_all_shards(self.transaction_pool)
            end_time = time.time()

            # Calculate TPS
            elapsed_time = end_time - start_time
            tps = num_transactions / elapsed_time
            results.append((shard_count, tps))
            print(f"Shard Count: {shard_count}, TPS: {tps:.2f}")

        # Ensure TPS increases with shard count
        for i in range(len(results) - 1):
            self.assertGreater(results[i+1][1], results[i][1], "TPS did not improve with additional shards")

    def test_cross_shard_consistency(self):
        """Ensures cross-shard transactions maintain consistency under high load."""
        num_transactions = 500
        shard_count = 8

        # Create shards
        self.shard_manager.clear_shards()
        for i in range(shard_count):
            self.shard_manager.create_shard(f"shard{i+1}")

        # Generate cross-shard transactions
        transactions = self.generate_transactions(num_transactions, shard_count)
        for tx in transactions:
            self.transaction_pool.add_transaction(tx, sender_balance=1000)

        # Process transactions
        self.shard_manager.process_all_shards(self.transaction_pool)

        # Verify balances across shards
        for tx in transactions:
            sender_shard = tx["sender"].split("@")[1]
            receiver_shard = tx["receiver"].split("@")[1]
            self.assertEqual(
                self.shard_manager.get_shard(sender_shard).blockchain.get_balance(tx["sender"].split("@")[0]), 990,
                f"Incorrect balance in {sender_shard} for {tx['sender']}"
            )
            self.assertEqual(
                self.shard_manager.get_shard(receiver_shard).blockchain.get_balance(tx["receiver"].split("@")[0]), 10,
                f"Incorrect balance in {receiver_shard} for {tx['receiver']}"
            )

if __name__ == "__main__":
    unittest.main()
