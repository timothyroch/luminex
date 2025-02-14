import json
import hashlib
import time
from blockchain.blocks.block import Block

class CrossShardCommunication:
    """Handles communication and data synchronization between shards in a sharded blockchain."""

    def __init__(self):
        self.message_queue = []  # Stores messages exchanged between shards

    def create_cross_shard_transaction(self, source_shard, destination_shard, transaction):
        """
        Initiates a cross-shard transaction.
        :param source_shard: The ID of the source shard.
        :param destination_shard: The ID of the destination shard.
        :param transaction: The transaction to send.
        :return: A dictionary representing the cross-shard message.
        """
        message = {
            "type": "cross_shard_transaction",
            "source_shard": source_shard,
            "destination_shard": destination_shard,
            "transaction": transaction,
            "timestamp": int(time.time()),
            "message_id": self._generate_message_id(transaction)
        }
        self.message_queue.append(message)
        print(f"Cross-shard transaction created: {message['message_id']}")
        return message

    def process_message(self, message, shard_manager):
        """
        Processes a cross-shard message.
        :param message: The message to process.
        :param shard_manager: The ShardManager instance for managing shards.
        """
        if message["type"] == "cross_shard_transaction":
            self._handle_cross_shard_transaction(message, shard_manager)
        else:
            print(f"Unknown message type: {message['type']}")

    def _handle_cross_shard_transaction(self, message, shard_manager):
        """
        Handles a cross-shard transaction.
        :param message: The cross-shard transaction message.
        :param shard_manager: The ShardManager instance.
        """
        destination_shard = message["destination_shard"]
        transaction = message["transaction"]

        # Simulate delivering the transaction to the destination shard
        if destination_shard in shard_manager.shard_metadata:
            shard_manager.assign_transaction_to_shard(transaction)
            print(f"Transaction delivered to shard {destination_shard}: {transaction}")
        else:
            print(f"Destination shard {destination_shard} not found.")

    def synchronize_state(self, source_shard, destination_shard, state_update):
        """
        Synchronizes state between shards.
        :param source_shard: The ID of the source shard.
        :param destination_shard: The ID of the destination shard.
        :param state_update: The state update to synchronize.
        """
        message = {
            "type": "state_sync",
            "source_shard": source_shard,
            "destination_shard": destination_shard,
            "state_update": state_update,
            "timestamp": int(time.time()),
            "message_id": self._generate_message_id(state_update)
        }
        self.message_queue.append(message)
        print(f"State synchronization message created: {message['message_id']}")

    def _generate_message_id(self, data):
        """
        Generates a unique message ID.
        :param data: The data to hash for the message ID.
        :return: A unique message ID as a hexadecimal string.
        """
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode("utf-8")).hexdigest()

    def get_pending_messages(self):
        """
        Retrieves all pending messages in the queue.
        :return: A list of pending messages.
        """
        return self.message_queue

    def clear_processed_messages(self):
        """
        Clears all processed messages from the queue.
        """
        self.message_queue = []
        print("All processed messages cleared.")

# Example usage
if __name__ == "__main__":
    from blockchain.sharding.shard_manager import ShardManager

    # Initialize ShardManager and CrossShardCommunication
    shard_manager = ShardManager(shard_count=2, max_transactions_per_shard=5)
    cross_shard_comm = CrossShardCommunication()

    # Simulate nodes joining shards
    shard_manager.assign_node_to_shard("node_1")
    shard_manager.assign_node_to_shard("node_2")

    # Create a cross-shard transaction
    transaction = {"sender": "Alice", "receiver": "Bob", "amount": 100}
    source_shard = "shard_0"
    destination_shard = "shard_1"
    message = cross_shard_comm.create_cross_shard_transaction(source_shard, destination_shard, transaction)

    # Process the message
    cross_shard_comm.process_message(message, shard_manager)

    # Synchronize state between shards
    state_update = {"balance": {"Bob": 100}}
    cross_shard_comm.synchronize_state(source_shard, destination_shard, state_update)

    # View pending messages
    print("Pending Messages:", cross_shard_comm.get_pending_messages())

    # Clear processed messages
    cross_shard_comm.clear_processed_messages()
