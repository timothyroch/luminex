import os
import json
import shutil
from pathlib import Path
import time
import plyvel  # type: ignore # LevelDB library for Python

class StateDB:
    """Manages persistent storage for blockchain state data."""

    def __init__(self, db_path="blockchain/state/storage/state_db"):
        """
        Initializes the StateDB.
        :param db_path: Path to the database directory.
        """
        self.db_path = Path(db_path)
        self.db = plyvel.DB(str(self.db_path), create_if_missing=True)

    def set_value(self, key, value):
        """
        Stores a key-value pair in the database.
        :param key: The key (string).
        :param value: The value (any serializable data).
        """
        key_bytes = key.encode("utf-8")
        value_bytes = json.dumps(value).encode("utf-8")
        self.db.put(key_bytes, value_bytes)

    def get_value(self, key):
        """
        Retrieves a value by key from the database.
        :param key: The key (string).
        :return: The value (deserialized), or None if the key is not found.
        """
        key_bytes = key.encode("utf-8")
        value_bytes = self.db.get(key_bytes)
        if value_bytes:
            return json.loads(value_bytes.decode("utf-8"))
        return None

    def delete_value(self, key):
        """
        Deletes a key-value pair from the database.
        :param key: The key to delete.
        """
        key_bytes = key.encode("utf-8")
        self.db.delete(key_bytes)

    def iterate_all(self):
        """
        Iterates over all key-value pairs in the database.
        :return: A generator yielding (key, value) tuples.
        """
        with self.db.iterator() as it:
            for key_bytes, value_bytes in it:
                key = key_bytes.decode("utf-8")
                value = json.loads(value_bytes.decode("utf-8"))
                yield key, value

    def backup(self, backup_path="blockchain/state/storage/backups"):
        """
        Creates a backup of the current database.
        :param backup_path: Path to the backup directory.
        """
        backup_dir = Path(backup_path)
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_file = backup_dir / f"state_backup_{int(time.time())}.tar.gz"
        shutil.make_archive(str(backup_file).replace(".tar.gz", ""), 'gztar', str(self.db_path))
        print(f"Backup created at: {backup_file}")

    def restore(self, backup_file):
        """
        Restores the database from a backup file.
        :param backup_file: Path to the backup file (tar.gz).
        """
        if self.db is not None:
            self.db.close()
        shutil.rmtree(self.db_path, ignore_errors=True)
        shutil.unpack_archive(backup_file, str(self.db_path))
        self.db = plyvel.DB(str(self.db_path), create_if_missing=False)
        print(f"Database restored from: {backup_file}")

    def close(self):
        """
        Closes the database connection.
        """
        self.db.close()


# Example usage
if __name__ == "__main__":
    # Initialize the StateDB
    state_db = StateDB()

    # Example data
    balances = {"Alice": 100, "Bob": 50}
    utxo_set = {
        ("tx1", 0): {"receiver": "Alice", "amount": 50},
        ("tx1", 1): {"receiver": "Bob", "amount": 30}
    }
    contracts = {
        "contract1": {"creator": "Alice", "state": {"token_balance": 1000}}
    }

    # Store values
    state_db.set_value("balances", balances)
    state_db.set_value("utxo_set", utxo_set)
    state_db.set_value("contracts", contracts)

    # Retrieve values
    print("Balances:", state_db.get_value("balances"))
    print("UTXO Set:", state_db.get_value("utxo_set"))
    print("Contracts:", state_db.get_value("contracts"))

    # Backup the database
    state_db.backup()

    # Iterate over all stored data
    print("\nStored Data:")
    for key, value in state_db.iterate_all():
        print(f"{key}: {value}")

    # Close the database
    state_db.close()
