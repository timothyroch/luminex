import os
import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # type: ignore
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC # type: ignore
from cryptography.hazmat.primitives import hashes # type: ignore
from cryptography.hazmat.backends import default_backend # type: ignore
from cryptography.hazmat.primitives.padding import PKCS7 # type: ignore
import base64
import logging

from blockchain.network.protocols.encryption.key_exchange import KeyExchange

# Configure logging
logging.basicConfig(
    filename="monitoring/logs/secure_channel.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

class SecureChannel:
    """Manages secure communication between two peers."""

    def __init__(self, peer_address):
        """
        Initializes the SecureChannel.
        :param peer_address: Address of the peer (IP, port).
        """
        self.peer_address = peer_address
        self.shared_key = None
        self.salt = os.urandom(16)  # Salt for key derivation
        self.key_exchange = KeyExchange()

    def establish_channel(self, peer_public_key_pem):
        """
        Establishes a secure channel by performing key exchange and deriving a shared key.
        :param peer_public_key_pem: The peer's public key in PEM format.
        """
        self.shared_key = self.key_exchange.generate_shared_secret(peer_public_key_pem)
        logging.info(f"Secure channel established with {self.peer_address}")

    def _derive_symmetric_key(self, shared_secret):
        """
        Derives a symmetric key from the shared secret.
        :param shared_secret: The shared secret from key exchange.
        :return: A symmetric encryption key.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(shared_secret)

    def encrypt_message(self, plaintext):
        """
        Encrypts a message using the derived symmetric key.
        :param plaintext: The message to encrypt.
        :return: The encrypted message (base64 encoded).
        """
        if not self.shared_key:
            raise ValueError("Secure channel not established. Call establish_channel() first.")

        key = self._derive_symmetric_key(self.shared_key)
        iv = os.urandom(16)  # Initialization vector
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Pad the plaintext and encrypt
        padder = PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        # Return IV + encrypted data as base64
        encrypted_message = base64.b64encode(iv + encrypted).decode("utf-8")
        logging.info("Message encrypted successfully.")
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        """
        Decrypts a message using the derived symmetric key.
        :param encrypted_message: The encrypted message (base64 encoded).
        :return: The decrypted plaintext.
        """
        if not self.shared_key:
            raise ValueError("Secure channel not established. Call establish_channel() first.")

        key = self._derive_symmetric_key(self.shared_key)
        encrypted_data = base64.b64decode(encrypted_message)
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]

        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt and unpad the ciphertext
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = PKCS7(128).unpadder()
        plaintext = unpadder.update(decrypted_padded) + unpadder.finalize()

        logging.info("Message decrypted successfully.")
        return plaintext.decode("utf-8")

# Example usage
if __name__ == "__main__":
    # Simulate Node A and Node B exchanging keys and establishing a secure channel

    # Node A
    node_a = KeyExchange()
    public_key_a = node_a.get_public_key()

    # Node B
    node_b = KeyExchange()
    public_key_b = node_b.get_public_key()

    # Node A establishes secure channel with Node B
    secure_channel_a = SecureChannel(peer_address=("127.0.0.1", 5001))
    secure_channel_a.establish_channel(public_key_b)

    # Node B establishes secure channel with Node A
    secure_channel_b = SecureChannel(peer_address=("127.0.0.1", 5000))
    secure_channel_b.establish_channel(public_key_a)

    # Node A sends encrypted message to Node B
    message = "Hello, secure world!"
    encrypted_message = secure_channel_a.encrypt_message(message)
    print(f"Encrypted message: {encrypted_message}")

    # Node B decrypts the received message
    decrypted_message = secure_channel_b.decrypt_message(encrypted_message)
    print(f"Decrypted message: {decrypted_message}")
