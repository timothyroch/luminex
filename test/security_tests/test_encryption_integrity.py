import unittest
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # type: ignore
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC # type: ignore
from cryptography.hazmat.primitives import hashes # type: ignore
from cryptography.hazmat.primitives import serialization # type: ignore
from cryptography.hazmat.backends import default_backend # type: ignore
import os

class TestEncryptionIntegrity(unittest.TestCase):
    def setUp(self):
        """Set up test data and encryption utilities."""
        self.password = b"securepassword"
        self.salt = os.urandom(16)
        self.backend = default_backend()

        # Derive a key from the password
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=self.backend
        )
        self.key = self.kdf.derive(self.password)

    def encrypt_data(self, plaintext):
        """Encrypts data using AES in GCM mode."""
        iv = os.urandom(12)
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        return iv, ciphertext, encryptor.tag

    def decrypt_data(self, iv, ciphertext, tag):
        """Decrypts data using AES in GCM mode."""
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv, tag), backend=self.backend)
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()

    def test_key_encryption(self):
        """Tests that private keys can be securely encrypted and decrypted."""
        private_key = os.urandom(32)  # Simulated private key
        iv, ciphertext, tag = self.encrypt_data(private_key)
        decrypted_key = self.decrypt_data(iv, ciphertext, tag)
        self.assertEqual(private_key, decrypted_key, "Decrypted key does not match the original key.")

    def test_transaction_encryption(self):
        """Tests that transaction payloads can be securely encrypted and decrypted."""
        transaction = b"Sender: Alice, Receiver: Bob, Amount: 50"
        iv, ciphertext, tag = self.encrypt_data(transaction)
        decrypted_transaction = self.decrypt_data(iv, ciphertext, tag)
        self.assertEqual(transaction, decrypted_transaction, "Decrypted transaction does not match the original payload.")

    def test_block_hash_integrity(self):
        """Tests that block data matches its cryptographic hash."""
        block_data = b"Block Index: 1, Previous Hash: abc123, Transactions: [...]"
        block_hash = hashes.Hash(hashes.SHA256(), backend=self.backend)
        block_hash.update(block_data)
        digest = block_hash.finalize()

        # Recalculate hash and compare
        recalculated_hash = hashes.Hash(hashes.SHA256(), backend=self.backend)
        recalculated_hash.update(block_data)
        self.assertEqual(digest, recalculated_hash.finalize(), "Block hash integrity check failed.")

if __name__ == "__main__":
    unittest.main()
