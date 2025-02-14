from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC # type: ignore
from cryptography.hazmat.primitives import hashes # type: ignore
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # type: ignore
from cryptography.hazmat.backends import default_backend # type: ignore
from cryptography.hazmat.primitives import padding # type: ignore
import os
import base64
import json

class KeyStorage:
    """Securely stores and retrieves private keys using encryption."""

    def __init__(self, storage_path="keys/", encryption_key=None):
        """
        Initializes the KeyStorage with a path for storing keys and an encryption key.
        :param storage_path: The directory for storing keys.
        :param encryption_key: The key used for encryption and decryption.
        """
        self.storage_path = storage_path
        self.encryption_key = self._derive_key(encryption_key or "default_encryption_key")
        os.makedirs(self.storage_path, exist_ok=True)

    def _derive_key(self, password):
        """
        Derives a secure key from a password.
        :param password: The password for key derivation.
        :return: A 32-byte encryption key.
        """
        salt = b"blockchain_salt"  # Use a secure, random salt in production
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

    def _encrypt(self, plaintext):
        """
        Encrypts plaintext using AES.
        :param plaintext: The plaintext to encrypt.
        :return: A base64-encoded encrypted string.
        """
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.encryption_key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padded_data = self._pad(plaintext.encode("utf-8"))
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(iv + ciphertext).decode("utf-8")

    def _decrypt(self, encrypted_data):
        """
        Decrypts data using AES.
        :param encrypted_data: The base64-encoded encrypted data.
        :return: The decrypted plaintext.
        """
        encrypted_bytes = base64.b64decode(encrypted_data)
        iv = encrypted_bytes[:16]
        ciphertext = encrypted_bytes[16:]
        cipher = Cipher(algorithms.AES(self.encryption_key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        return self._unpad(padded_data).decode("utf-8")

    def _pad(self, data):
        """
        Pads data to make it a multiple of the block size.
        :param data: The data to pad.
        :return: Padded data.
        """
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        return padder.update(data) + padder.finalize()

    def _unpad(self, padded_data):
        """
        Removes padding from data.
        :param padded_data: The padded data.
        :return: Unpadded data.
        """
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()

    def store_key(self, key_name, private_key):
        """
        Encrypts and stores a private key in a file.
        :param key_name: The name of the key (used as the filename).
        :param private_key: The private key in PEM format.
        """
        encrypted_key = self._encrypt(private_key)
        with open(os.path.join(self.storage_path, f"{key_name}.key"), "w") as file:
            file.write(encrypted_key)
        print(f"Key '{key_name}' stored securely.")

    def retrieve_key(self, key_name):
        """
        Retrieves and decrypts a private key from storage.
        :param key_name: The name of the key to retrieve.
        :return: The decrypted private key in PEM format.
        """
        file_path = os.path.join(self.storage_path, f"{key_name}.key")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Key '{key_name}' not found.")
        with open(file_path, "r") as file:
            encrypted_key = file.read()
        return self._decrypt(encrypted_key)

    def list_keys(self):
        """
        Lists all stored keys in the storage path.
        :return: A list of key names.
        """
        return [f.split(".key")[0] for f in os.listdir(self.storage_path) if f.endswith(".key")]

    def delete_key(self, key_name):
        """
        Deletes a stored key.
        :param key_name: The name of the key to delete.
        """
        file_path = os.path.join(self.storage_path, f"{key_name}.key")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Key '{key_name}' deleted.")
        else:
            print(f"Key '{key_name}' not found.")


# Example usage
if __name__ == "__main__":
    key_storage = KeyStorage()

    # Example private key in PEM format (replace with a real key in production)
    private_key = """-----BEGIN PRIVATE KEY-----
MIIBVgIBADANBgkqhkiG9w0BAQEFAASCATwwggE4AgEAAkEAxjJ+nXcQLR2NNeHF
...
-----END PRIVATE KEY-----"""

    # Store the key
    key_storage.store_key("user1", private_key)

    # Retrieve the key
    retrieved_key = key_storage.retrieve_key("user1")
    print("Retrieved Key:\n", retrieved_key)

    # List all stored keys
    print("Stored Keys:", key_storage.list_keys())

    # Delete the key
    key_storage.delete_key("user1")
