import hashlib
import json
import time
import hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # type: ignore
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC # type: ignore
from cryptography.hazmat.primitives import hashes # type: ignore
from cryptography.hazmat.backends import default_backend # type: ignore
import os

class ShardProtocols:
    """Defines secure communication protocols for shard-level data exchange."""

    def __init__(self, secret_key):
        """
        Initializes the ShardProtocols with a shared secret key for encryption and authentication.
        :param secret_key: The shared secret key used for HMAC and encryption.
        """
        self.secret_key = secret_key

    def create_message(self, message_type, source_shard, destination_shard, payload):
        """
        Creates a secure message following the shard communication protocol.
        :param message_type: The type of the message (e.g., "cross_shard_transaction").
        :param source_shard: The source shard ID.
        :param destination_shard: The destination shard ID.
        :param payload: The message payload.
        :return: A dictionary representing the secure message.
        """
        timestamp = int(time.time())
        payload_encrypted = self._encrypt_payload(payload)
        message_id = self._generate_message_id(message_type, source_shard, destination_shard, payload, timestamp)
        hmac_signature = self._generate_hmac(message_id)

        message = {
            "type": message_type,
            "source_shard": source_shard,
            "destination_shard": destination_shard,
            "timestamp": timestamp,
            "payload_encrypted": payload_encrypted,
            "message_id": message_id,
            "hmac_signature": hmac_signature
        }

        return message

    def verify_message(self, message):
        """
        Verifies the authenticity and integrity of a received message.
        :param message: The received message.
        :return: True if the message is valid, False otherwise.
        """
        try:
            # Verify HMAC signature
            expected_hmac = self._generate_hmac(message["message_id"])
            if not hmac.compare_digest(expected_hmac, message["hmac_signature"]):
                print("Invalid HMAC signature.")
                return False

            # Check timestamp for freshness
            current_time = time.time()
            if abs(current_time - message["timestamp"]) > 300:  # 5-minute tolerance
                print("Message timestamp is outside the valid range.")
                return False

            print("Message verification successful.")
            return True

        except Exception as e:
            print(f"Message verification failed: {e}")
            return False

    def decrypt_payload(self, encrypted_payload):
        """
        Decrypts the encrypted payload from a message.
        :param encrypted_payload: The encrypted payload.
        :return: The decrypted payload as a dictionary.
        """
        return self._decrypt_payload(encrypted_payload)

    def _generate_message_id(self, message_type, source_shard, destination_shard, payload, timestamp):
        """
        Generates a unique message ID based on the message content.
        :param message_type: The type of the message.
        :param source_shard: The source shard ID.
        :param destination_shard: The destination shard ID.
        :param payload: The message payload.
        :param timestamp: The message timestamp.
        :return: A unique message ID.
        """
        data_str = f"{message_type}{source_shard}{destination_shard}{json.dumps(payload, sort_keys=True)}{timestamp}"
        return hashlib.sha256(data_str.encode("utf-8")).hexdigest()

    def _generate_hmac(self, message_id):
        """
        Generates an HMAC signature for a given message ID.
        :param message_id: The message ID.
        :return: The HMAC signature as a hexadecimal string.
        """
        hmac_obj = hmac.new(self.secret_key.encode("utf-8"), message_id.encode("utf-8"), hashlib.sha256)
        return hmac_obj.hexdigest()

    def _encrypt_payload(self, payload):
        """
        Encrypts the payload using AES encryption.
        :param payload: The payload to encrypt.
        :return: The encrypted payload as a hexadecimal string.
        """
        salt = os.urandom(16)
        key = self._derive_key(self.secret_key, salt)
        iv = os.urandom(16)

        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        payload_bytes = json.dumps(payload).encode("utf-8")
        encrypted_payload = encryptor.update(payload_bytes) + encryptor.finalize()

        return json.dumps({"salt": salt.hex(), "iv": iv.hex(), "data": encrypted_payload.hex()})

    def _decrypt_payload(self, encrypted_payload):
        """
        Decrypts an AES-encrypted payload.
        :param encrypted_payload: The encrypted payload as a JSON string.
        :return: The decrypted payload as a dictionary.
        """
        encrypted_data = json.loads(encrypted_payload)
        salt = bytes.fromhex(encrypted_data["salt"])
        iv = bytes.fromhex(encrypted_data["iv"])
        encrypted_bytes = bytes.fromhex(encrypted_data["data"])

        key = self._derive_key(self.secret_key, salt)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_payload = decryptor.update(encrypted_bytes) + decryptor.finalize()

        return json.loads(decrypted_payload.decode("utf-8"))

    def _derive_key(self, password, salt):
        """
        Derives a cryptographic key from a password and salt.
        :param password: The password to derive the key from.
        :param salt: The salt for the key derivation.
        :return: The derived key.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode("utf-8"))


# Example usage
if __name__ == "__main__":
    secret_key = "super_secure_shared_key"
    shard_protocols = ShardProtocols(secret_key)

    # Create a secure message
    payload = {"sender": "Alice", "receiver": "Bob", "amount": 100}
    message = shard_protocols.create_message("cross_shard_transaction", "shard_0", "shard_1", payload)
    print("Created Message:", message)

    # Verify the message
    is_valid = shard_protocols.verify_message(message)
    print("Message Valid:", is_valid)

    # Decrypt the payload
    decrypted_payload = shard_protocols.decrypt_payload(message["payload_encrypted"])
    print("Decrypted Payload:", decrypted_payload)
