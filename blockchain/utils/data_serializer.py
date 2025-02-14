import json
import pickle
import zlib
from typing import Any

class DataSerializer:
    """Handles serialization, deserialization, and optional compression of blockchain data."""

    @staticmethod
    def serialize_to_json(data: Any) -> str:
        """
        Serializes data to a JSON string.
        :param data: The data to serialize (must be JSON-serializable).
        :return: The serialized JSON string.
        """
        try:
            return json.dumps(data, indent=4, sort_keys=True)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to serialize to JSON: {e}")

    @staticmethod
    def deserialize_from_json(json_data: str) -> Any:
        """
        Deserializes data from a JSON string.
        :param json_data: The JSON string to deserialize.
        :return: The original data structure.
        """
        try:
            return json.loads(json_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to deserialize from JSON: {e}")

    @staticmethod
    def serialize_to_binary(data: Any) -> bytes:
        """
        Serializes data to a binary format using pickle.
        :param data: The data to serialize.
        :return: The serialized binary data.
        """
        try:
            return pickle.dumps(data)
        except pickle.PickleError as e:
            raise ValueError(f"Failed to serialize to binary: {e}")

    @staticmethod
    def deserialize_from_binary(binary_data: bytes) -> Any:
        """
        Deserializes data from a binary format using pickle.
        :param binary_data: The binary data to deserialize.
        :return: The original data structure.
        """
        try:
            return pickle.loads(binary_data)
        except pickle.PickleError as e:
            raise ValueError(f"Failed to deserialize from binary: {e}")

    @staticmethod
    def compress_data(data: bytes) -> bytes:
        """
        Compresses binary data using zlib.
        :param data: The binary data to compress.
        :return: The compressed binary data.
        """
        try:
            return zlib.compress(data)
        except zlib.error as e:
            raise ValueError(f"Failed to compress data: {e}")

    @staticmethod
    def decompress_data(compressed_data: bytes) -> bytes:
        """
        Decompresses binary data using zlib.
        :param compressed_data: The compressed binary data.
        :return: The original binary data.
        """
        try:
            return zlib.decompress(compressed_data)
        except zlib.error as e:
            raise ValueError(f"Failed to decompress data: {e}")


# Example usage
if __name__ == "__main__":
    # Sample data
    data = {
        "block": {
            "index": 1,
            "timestamp": "2025-01-10T16:00:00",
            "transactions": [
                {"sender": "Alice", "receiver": "Bob", "amount": 50},
                {"sender": "Charlie", "receiver": "Dave", "amount": 30}
            ],
            "previous_hash": "0xabcdef",
            "nonce": 12345
        }
    }

    # Serialize to JSON
    json_data = DataSerializer.serialize_to_json(data)
    print("Serialized to JSON:\n", json_data)

    # Deserialize from JSON
    deserialized_data = DataSerializer.deserialize_from_json(json_data)
    print("Deserialized from JSON:\n", deserialized_data)

    # Serialize to binary
    binary_data = DataSerializer.serialize_to_binary(data)
    print("Serialized to Binary:", binary_data)

    # Deserialize from binary
    deserialized_binary_data = DataSerializer.deserialize_from_binary(binary_data)
    print("Deserialized from Binary:\n", deserialized_binary_data)

    # Compress binary data
    compressed_data = DataSerializer.compress_data(binary_data)
    print("Compressed Data:", compressed_data)

    # Decompress binary data
    decompressed_data = DataSerializer.decompress_data(compressed_data)
    print("Decompressed Data:\n", DataSerializer.deserialize_from_binary(decompressed_data))
