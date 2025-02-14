import hashlib
import json

class UTXOSet:
    """Manages the Unspent Transaction Output (UTXO) set."""

    def __init__(self, initial_utxos=None):
        """
        Initializes the UTXOSet.
        :param initial_utxos: A list of initial UTXOs for the genesis state.
        """
        self.utxos = initial_utxos or {}

    def apply_transaction(self, transaction):
        """
        Updates the UTXO set based on a transaction.
        :param transaction: The transaction to apply.
        """
        tx_id = self._get_transaction_id(transaction)

        # Remove spent UTXOs
        for input_utxo in transaction["inputs"]:
            self._remove_utxo(input_utxo["tx_id"], input_utxo["index"])

        # Add new UTXOs
        for index, output in enumerate(transaction["outputs"]):
            self._add_utxo(tx_id, index, output)

    def rollback_transaction(self, transaction):
        """
        Rolls back a transaction, restoring spent UTXOs and removing newly created ones.
        :param transaction: The transaction to rollback.
        """
        tx_id = self._get_transaction_id(transaction)

        # Restore spent UTXOs
        for input_utxo in transaction["inputs"]:
            self._add_utxo(input_utxo["tx_id"], input_utxo["index"], input_utxo)

        # Remove newly created UTXOs
        for index in range(len(transaction["outputs"])):
            self._remove_utxo(tx_id, index)

    def _add_utxo(self, tx_id, index, output):
        """
        Adds a UTXO to the set.
        :param tx_id: The transaction ID.
        :param index: The index of the output in the transaction.
        :param output: The output details.
        """
        self.utxos[(tx_id, index)] = output

    def _remove_utxo(self, tx_id, index):
        """
        Removes a UTXO from the set.
        :param tx_id: The transaction ID.
        :param index: The index of the output in the transaction.
        """
        self.utxos.pop((tx_id, index), None)

    def get_utxos(self, address):
        """
        Retrieves all UTXOs for a specific address.
        :param address: The address to query.
        :return: A list of UTXOs for the address.
        """
        return [output for output in self.utxos.values() if output["receiver"] == address]

    def validate_transaction(self, transaction):
        """
        Validates a transaction against the current UTXO set.
        :param transaction: The transaction to validate.
        :return: True if the transaction is valid, False otherwise.
        """
        input_sum = 0
        output_sum = sum(output["amount"] for output in transaction["outputs"])

        for input_utxo in transaction["inputs"]:
            utxo = self.utxos.get((input_utxo["tx_id"], input_utxo["index"]))
            if not utxo:
                print(f"Invalid input: {input_utxo}")
                return False
            if utxo["receiver"] != transaction["sender"]:
                print(f"UTXO not owned by sender: {input_utxo}")
                return False
            input_sum += utxo["amount"]

        # Ensure input sum covers output sum plus fee
        fee = transaction.get("fee", 0)
        if input_sum < output_sum + fee:
            print("Insufficient input value.")
            return False

        return True

    def get_state(self):
        """
        Returns the current UTXO set as a dictionary.
        :return: The current UTXO set.
        """
        return self.utxos

    @staticmethod
    def _get_transaction_id(transaction):
        """
        Computes the transaction ID as a SHA-256 hash of the transaction.
        :param transaction: The transaction to hash.
        :return: The transaction ID as a hexadecimal string.
        """
        transaction_data = json.dumps(transaction, sort_keys=True)
        return hashlib.sha256(transaction_data.encode("utf-8")).hexdigest()


# Example usage
if __name__ == "__main__":
    # Example initial UTXOs
    initial_utxos = {
        ("tx1", 0): {"receiver": "Alice", "amount": 50},
        ("tx1", 1): {"receiver": "Bob", "amount": 30}
    }

    utxo_set = UTXOSet(initial_utxos)

    # Example transaction
    transaction = {
        "sender": "Alice",
        "inputs": [{"tx_id": "tx1", "index": 0}],
        "outputs": [
            {"receiver": "Bob", "amount": 40},
            {"receiver": "Alice", "amount": 9}
        ],
        "fee": 1
    }

    # Validate transaction
    if utxo_set.validate_transaction(transaction):
        print("Transaction is valid.")
        utxo_set.apply_transaction(transaction)
    else:
        print("Transaction is invalid.")

    # Display UTXOs
    print("Updated UTXO set:", utxo_set.get_state())
