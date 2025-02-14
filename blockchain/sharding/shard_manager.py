import hashlib
import json
import time
from collections import defaultdict

class ShardManager:
    """Manages shard assignment, creation, and maintenance in a sharded blockchain."""

    def __init__(self, shard_count=4, max_transactions_per_shard=1000):
        """
        Initializes the ShardManager.
        :param shard_count: Initial number of shards.
        :param max_transactions_per_shard: Maximum number of pending transactions per shard.
        """
        self.shard_count = shard_count
        self.max_transactions_per_shard = max_transactions_per_shard
        self.shard_metadata = self._initialize_shards()
        self.shard_transactions = defaultdict(list)
        self.node_assignments = defaultdict(set)  # Maps shard ID to nodes

    def _initialize_shards(self):
        """
        Initializes shard metadata.
        :return: A dictionary containing metadata for each shard.
        """
        return {
            f"shard_{i}": {
                "id": f"shard_{i}",
                "created_at": time.time(),
                "nodes": set(),
                "transaction_count": 0
            }
            for i in range(self.shard_count)
        }

    def assign_transaction_to_shard(self, transaction):
        """
        Assigns a transaction to the appropriate shard based on its sender.
        :param transaction: The transaction to assign.
        :return: The ID of the assigned shard.
        """
        sender_hash = hashlib.sha256(transaction["sender"].encode()).hexdigest()
        shard_id = f"shard_{int(sender_hash, 16) % self.shard_count}"

        # Ensure shard capacity
        if len(self.shard_transactions[shard_id]) < self.max_transactions_per_shard:
            self.shard_transactions[shard_id].append(transaction)
            self.shard_metadata[shard_id]["transaction_count"] += 1
            print(f"Transaction assigned to {shard_id}")
        else:
            print(f"Shard {shard_id} is at capacity.")
            shard_id = self._create_new_shard()
            self.assign_transaction_to_shard(transaction)  # Retry assignment

        return shard_id

    def assign_node_to_shard(self, node_id):
        """
        Assigns a node to a shard.
        :param node_id: The ID of the node.
        :return: The ID of the shard the node was assigned to.
        """
        shard_id = min(
            self.shard_metadata.keys(),
            key=lambda s: len(self.node_assignments[s])
        )
        self.node_assignments[shard_id].add(node_id)
        self.shard_metadata[shard_id]["nodes"].add(node_id)
        print(f"Node {node_id} assigned to {shard_id}")
        return shard_id

    def _create_new_shard(self):
        """
        Creates a new shard when existing shards are at capacity.
        :return: The ID of the new shard.
        """
        new_shard_id = f"shard_{self.shard_count}"
        self.shard_metadata[new_shard_id] = {
            "id": new_shard_id,
            "created_at": time.time(),
            "nodes": set(),
            "transaction_count": 0
        }
        self.shard_count += 1
        print(f"New shard created: {new_shard_id}")
        return new_shard_id

    def delete_shard(self, shard_id):
        """
        Deletes a shard and redistributes its transactions and nodes.
        :param shard_id: The ID of the shard to delete.
        """
        if shard_id not in self.shard_metadata:
            print(f"Shard {shard_id} does not exist.")
            return

        # Redistribute transactions
        for transaction in self.shard_transactions[shard_id]:
            self.assign_transaction_to_shard(transaction)

        # Redistribute nodes
        for node in self.node_assignments[shard_id]:
            self.assign_node_to_shard(node)

        # Remove shard data
        del self.shard_metadata[shard_id]
        del self.shard_transactions[shard_id]
        del self.node_assignments[shard_id]
        print(f"Shard {shard_id} deleted.")

    def get_shard_metadata(self):
        """
        Retrieves metadata for all shards.
        :return: A dictionary containing shard metadata.
        """
        return self.shard_metadata

    def monitor_shards(self):
        """
        Monitors shard performance and prints shard stats.
        """
        for shard_id, metadata in self.shard_metadata.items():
            print(f"Shard {shard_id}: {metadata['transaction_count']} transactions, {len(metadata['nodes'])} nodes")


# Example usage
if __name__ == "__main__":
    shard_manager = ShardManager(shard_count=2, max_transactions_per_shard=3)

    # Simulate nodes joining the network
    shard_manager.assign_node_to_shard("node_1")
    shard_manager.assign_node_to_shard("node_2")

    # Simulate transactions
    transactions = [
        {"sender": "Alice", "receiver": "Bob", "amount": 10},
        {"sender": "Charlie", "receiver": "Dave", "amount": 20},
        {"sender": "Eve", "receiver": "Frank", "amount": 30},
        {"sender": "Grace", "receiver": "Hank", "amount": 40}
    ]

    for tx in transactions:
        shard_manager.assign_transaction_to_shard(tx)

    # Monitor shard performance
    shard_manager.monitor_shards()

    # Create a new shard
    new_shard_id = shard_manager._create_new_shard()
    print(f"New shard created: {new_shard_id}")

    # Delete a shard
    shard_manager.delete_shard("shard_0")

    # View shard metadata
    print("Shard Metadata:", shard_manager.get_shard_metadata())
