import os
import json
import base64
import hashlib
from mnemonic import Mnemonic # type: ignore
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC # type: ignore
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # type: ignore
from cryptography.hazmat.backends import default_backend # type: ignore
from cryptography.hazmat.primitives import padding # type: ignore

class KeyRecovery:
    """Handles private key recovery using mnemonic phrases and encrypted backups."""

    def __init__(self, recovery_path="backups/"):
        """
        Initializes the KeyRecovery with a path for storing and retrieving backups.
        :param recovery_path: The directory for storing encrypted key backups.
        """
        self.recovery_path = recovery_path
        os.makedirs(self.recovery_path, exist_ok=True)
        self.mnemonic = Mnemonic("english")

    def generate_mnemonic(self):
        """
        Generates a new mnemonic phrase.
        :return: A 12-word mnemonic phrase.
        """
        return self.mnemonic.generate(strength=128)  # Generates a 12-word mnemonic

    def mnemonic_to_seed(self, mnemonic_phrase, passphrase=""):
        """
        Converts a mnemonic phrase to a cryptographic seed.
        :param mnemonic_phrase: The mnemonic phrase.
        :param passphrase: An optional passphrase for additional security.
        :return: The derived seed as a hexadecimal string.
        """
        return self.mnemonic.to_seed(mnemonic_phrase, passphrase).hex()

    def encrypt_key(self, private_key, password):
        """
        Encrypts a private key using a password.
        :param private_key: The private key to encrypt.
        :param password: The password for encryption.
        :return: The encrypted private key as a base64-encoded string.
        """
        salt = os.urandom(16)
        iv = os.urandom(16)
        key = self._derive_key(password, salt)

        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padded_key = self._pad(private_key.encode("utf-8"))
        encrypted_key = encryptor.update(padded_key) + encryptor.finalize()

        encrypted_data = {
            "salt": base64.b64encode(salt).decode("utf-8"),
            "iv": base64.b64encode(iv).decode("utf-8"),
            "key": base64.b64encode(encrypted_key).decode("utf-8")
        }

        return json.dumps(encrypted_data)

    def decrypt_key(self, encrypted_data, password):
        """
        Decrypts an encrypted private key using a password.
        :param encrypted_data: The encrypted private key (JSON format).
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
        return self._unpad(padded_key).decode("utf-8")

    def backup_key(self, private_key, password, backup_name="backup"):
        """
        Creates an encrypted backup of a private key.
        :param private_key: The private key to back up.
        :param password: The password for encrypting the backup.
        :param backup_name: The name of the backup file.
        """
        encrypted_key = self.encrypt_key(private_key, password)
        backup_path = os.path.join(self.recovery_path, f"{backup_name}.json")
        with open(backup_path, "w") as backup_file:
            backup_file.write(encrypted_key)
        print(f"Backup created at: {backup_path}")

    def recover_key_from_backup(self, backup_name, password):
        """
        Recovers a private key from an encrypted backup.
        :param backup_name: The name of the backup file.
        :param password: The password for decrypting the backup.
        :return: The recovered private key.
        """
        backup_path = os.path.join(self.recovery_path, f"{backup_name}.json")
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup '{backup_name}' not found.")
        with open(backup_path, "r") as backup_file:
            encrypted_data = backup_file.read()
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
        return kdf.derive(password.encode("utf-8"))

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


# Example usage
if __name__ == "__main__":
    key_recovery = KeyRecovery()

    # Generate mnemonic phrase
    mnemonic = key_recovery.generate_mnemonic()
    print("Generated Mnemonic:", mnemonic)

    # Convert mnemonic to seed
    seed = key_recovery.mnemonic_to_seed(mnemonic)
    print("Derived Seed:", seed)

    # Example private key
    private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----"

    # Backup the private key
    key_recovery.backup_key(private_key, password="secure_password", backup_name="my_backup")

    # Recover the private key from backup
    recovered_key = key_recovery.recover_key_from_backup("my_backup", password="secure_password")
    print("Recovered Private Key:\n", recovered_key)
