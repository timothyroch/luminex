import hashlib
import json
import time
from collections import defaultdict

class ShardMessageHandler:
    """Manages shard-level messaging, including message validation, routing, and queue management."""

    def __init__(self):
        self.message_queue = defaultdict(list)  # Queue of messages for each shard
        self.processed_messages = set()  # Set of processed message IDs for deduplication

    def validate_message(self, message):
        """
        Validates the structure and integrity of a message.
        :param message: The message to validate.
        :return: True if the message is valid, False otherwise.
        """
        required_fields = ["type", "source_shard", "destination_shard", "timestamp", "payload", "message_id"]
        for field in required_fields:
            if field not in message:
                print(f"Invalid message: Missing field {field}")
                return False

        # Ensure the message ID is unique
        if message["message_id"] in self.processed_messages:
            print(f"Duplicate message detected: {message['message_id']}")
            return False

        # Check timestamp validity (e.g., not too far in the past or future)
        current_time = time.time()
        if abs(current_time - message["timestamp"]) > 300:  # Allow a 5-minute drift
            print(f"Invalid message timestamp: {message['timestamp']}")
            return False

        return True

    def route_message(self, message, shard_manager):
        """
        Routes a message to the appropriate destination shard.
        :param message: The message to route.
        :param shard_manager: The ShardManager instance.
        """
        destination_shard = message["destination_shard"]

        if destination_shard not in shard_manager.shard_metadata:
            print(f"Invalid destination shard: {destination_shard}")
            return False

        self.message_queue[destination_shard].append(message)
        print(f"Message routed to shard {destination_shard}: {message['message_id']}")
        return True

    def process_messages(self, shard_id, handler_callback):
        """
        Processes all queued messages for a specific shard.
        :param shard_id: The ID of the shard.
        :param handler_callback: A callback function to handle each message.
        """
        if shard_id not in self.message_queue:
            print(f"No messages for shard {shard_id}")
            return

        while self.message_queue[shard_id]:
            message = self.message_queue[shard_id].pop(0)
            if self.validate_message(message):
                handler_callback(message)
                self.processed_messages.add(message["message_id"])
                print(f"Processed message {message['message_id']} for shard {shard_id}")
            else:
                print(f"Failed to process message: {message}")

    def clear_processed_messages(self):
        """
        Clears the set of processed messages to free memory.
        """
        self.processed_messages.clear()
        print("Cleared all processed messages.")

    def create_message(self, message_type, source_shard, destination_shard, payload):
        """
        Creates a new message for shard-level communication.
        :param message_type: The type of the message (e.g., "cross_shard_transaction").
        :param source_shard: The ID of the source shard.
        :param destination_shard: The ID of the destination shard.
        :param payload: The message payload (data to be communicated).
        :return: A dictionary representing the message.
        """
        message = {
            "type": message_type,
            "source_shard": source_shard,
            "destination_shard": destination_shard,
            "timestamp": int(time.time()),
            "payload": payload,
            "message_id": self._generate_message_id(message_type, source_shard, destination_shard, payload)
        }
        return message

    def _generate_message_id(self, message_type, source_shard, destination_shard, payload):
        """
        Generates a unique message ID based on message content.
        :param message_type: The type of the message.
        :param source_shard: The source shard ID.
        :param destination_shard: The destination shard ID.
        :param payload: The payload of the message.
        :return: A unique message ID as a hexadecimal string.
        """
        data_str = f"{message_type}{source_shard}{destination_shard}{json.dumps(payload, sort_keys=True)}"
        return hashlib.sha256(data_str.encode("utf-8")).hexdigest()


# Example usage
if __name__ == "__main__":
    from blockchain.sharding.shard_manager import ShardManager

    # Initialize ShardManager and ShardMessageHandler
    shard_manager = ShardManager(shard_count=2)
    message_handler = ShardMessageHandler()

    # Simulate creating and routing a message
    message = message_handler.create_message(
        message_type="cross_shard_transaction",
        source_shard="shard_0",
        destination_shard="shard_1",
        payload={"sender": "Alice", "receiver": "Bob", "amount": 100}
    )
    message_handler.route_message(message, shard_manager)

    # Process messages for a specific shard
    def sample_handler(message):
        print(f"Handling message: {message}")

    message_handler.process_messages("shard_1", sample_handler)

    # Clear processed messages
    message_handler.clear_processed_messages()
