import os
import json
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC # type: ignore
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # type: ignore
from cryptography.hazmat.primitives import padding # type: ignore
from cryptography.hazmat.backends import default_backend # type: ignore
from cryptography.hazmat.primitives import hashes # type: ignore


class KeyStorage:
    """Securely stores and retrieves private keys."""

    def __init__(self, storage_path="keys/"):
        """
        Initializes the KeyStorage with a specified storage path.
        :param storage_path: Directory to store encrypted private keys.
        """
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)

    def encrypt_key(self, private_key, password):
        """
        Encrypts a private key using a password.
        :param private_key: The private key to encrypt (string).
        :param password: The password for encryption.
        :return: The encrypted private key as a JSON string.
        """
        salt = os.urandom(16)
        iv = os.urandom(16)
        key = self._derive_key(password, salt)

        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padded_key = self._pad(private_key.encode('utf-8'))
        encrypted_key = encryptor.update(padded_key) + encryptor.finalize()

        encrypted_data = {
            "salt": base64.b64encode(salt).decode('utf-8'),
            "iv": base64.b64encode(iv).decode('utf-8'),
            "key": base64.b64encode(encrypted_key).decode('utf-8')
        }

        return json.dumps(encrypted_data)

    def decrypt_key(self, encrypted_data, password):
        """
        Decrypts an encrypted private key using a password.
        :param encrypted_data: The encrypted private key (JSON string).
        :param password: The password for decryption.
        :return: The decrypted private key as a string.
        """
        encrypted_dict = json.loads(encrypted_data)
        salt = base64.b64decode(encrypted_dict["salt"])
        iv = base64.b64decode(encrypted_dict["iv"])
        encrypted_key = base64.b64decode(encrypted_dict["key"])
        key = self._derive_key(password, salt)

        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_key = decryptor.update(encrypted_key) + decryptor.finalize()
        return self._unpad(padded_key).decode('utf-8')

    def store_key(self, key_name, private_key, password):
        """
        Encrypts and stores a private key in a file.
        :param key_name: The name of the key (used as the filename).
        :param private_key: The private key to store.
        :param password: The password to encrypt the key.
        """
        encrypted_key = self.encrypt_key(private_key, password)
        file_path = os.path.join(self.storage_path, f"{key_name}.json")
        with open(file_path, "w") as file:
            file.write(encrypted_key)
        print(f"Key '{key_name}' stored securely at {file_path}.")

    def retrieve_key(self, key_name, password):
        """
        Retrieves and decrypts a private key from a file.
        :param key_name: The name of the key to retrieve.
        :param password: The password to decrypt the key.
        :return: The decrypted private key.
        """
        file_path = os.path.join(self.storage_path, f"{key_name}.json")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Key '{key_name}' not found.")
        with open(file_path, "r") as file:
            encrypted_data = file.read()
        return self.decrypt_key(encrypted_data, password)

    def _derive_key(self, password, salt):
        """
        Derives a cryptographic key from a password and salt.
        :param password: The password for key derivation.
        :param salt: The salt for key derivation.
        :return: The derived cryptographic key.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode('utf-8'))

    def _pad(self, data):
        """
        Pads data to make it compatible with AES block size.
        :param data: The data to pad.
        :return: Padded data.
        """
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        return padder.update(data) + padder.finalize()

    def _unpad(self, padded_data):
        """
        Removes padding from decrypted data.
        :param padded_data: The padded data.
        :return: Unpadded data.
        """
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()


# Example usage
if __name__ == "__main__":
    key_storage = KeyStorage()

    # Example private key
    private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----"

    # Store the private key
    key_storage.store_key("user1", private_key, "secure_password")

    # Retrieve the private key
    retrieved_key = key_storage.retrieve_key("user1", "secure_password")
    print("Retrieved Private Key:\n", retrieved_key)
