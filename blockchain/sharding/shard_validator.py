import hashlib
import json
import time

class ShardValidator:
    """Validates shard-specific blocks and transactions in a sharded blockchain."""

    def __init__(self, shard_id, shard_state):
        """
        Initializes the ShardValidator.
        :param shard_id: The ID of the shard this validator is responsible for.
        :param shard_state: The state of the shard, including UTXOs and balances.
        """
        self.shard_id = shard_id
        self.shard_state = shard_state

    def validate_block(self, block):
        """
        Validates a block's structure, transactions, and state transitions.
        :param block: The block to validate.
        :return: True if the block is valid, False otherwise.
        """
        try:
            # Validate block structure
            if not self._validate_block_structure(block):
                print(f"Invalid block structure for block {block['block_hash']}")
                return False

            # Validate each transaction in the block
            for transaction in block["transactions"]:
                if not self.validate_transaction(transaction):
                    print(f"Invalid transaction in block {block['block_hash']}: {transaction}")
                    return False

            # Validate state transitions
            if not self._validate_state_transitions(block):
                print(f"Invalid state transition in block {block['block_hash']}")
                return False

            print(f"Block {block['block_hash']} is valid.")
            return True

        except Exception as e:
            print(f"Block validation failed: {e}")
            return False

    def validate_transaction(self, transaction):
        """
        Validates a transaction's structure, inputs, and outputs.
        :param transaction: The transaction to validate.
        :return: True if the transaction is valid, False otherwise.
        """
        try:
            # Validate transaction structure
            if not self._validate_transaction_structure(transaction):
                return False

            # Check transaction inputs
            input_sum = 0
            for tx_input in transaction["inputs"]:
                utxo = self.shard_state["utxos"].get((tx_input["tx_id"], tx_input["index"]))
                if not utxo or utxo["receiver"] != transaction["sender"]:
                    print(f"Invalid input UTXO: {tx_input}")
                    return False
                input_sum += utxo["amount"]

            # Check transaction outputs
            output_sum = sum(output["amount"] for output in transaction["outputs"])
            if input_sum < output_sum + transaction.get("fee", 0):
                print(f"Insufficient input value in transaction: {transaction}")
                return False

            # Check digital signature (assuming it's a placeholder here)
            if not self._verify_signature(transaction):
                print("Invalid digital signature.")
                return False

            print(f"Transaction {transaction['tx_id']} is valid.")
            return True

        except Exception as e:
            print(f"Transaction validation failed: {e}")
            return False

    def _validate_block_structure(self, block):
        """
        Validates the basic structure of a block.
        :param block: The block to validate.
        :return: True if the block structure is valid, False otherwise.
        """
        required_fields = ["block_hash", "previous_hash", "timestamp", "transactions", "nonce"]
        for field in required_fields:
            if field not in block:
                print(f"Missing field in block: {field}")
                return False

        # Check timestamp validity
        if block["timestamp"] > time.time():
            print("Block timestamp is in the future.")
            return False

        return True

    def _validate_transaction_structure(self, transaction):
        """
        Validates the structure of a transaction.
        :param transaction: The transaction to validate.
        :return: True if the structure is valid, False otherwise.
        """
        required_fields = ["tx_id", "sender", "inputs", "outputs", "nonce"]
        for field in required_fields:
            if field not in transaction:
                print(f"Missing field in transaction: {field}")
                return False

        # Ensure inputs and outputs are properly formatted
        if not isinstance(transaction["inputs"], list) or not isinstance(transaction["outputs"], list):
            print("Inputs and outputs must be lists.")
            return False

        return True

    def _validate_state_transitions(self, block):
        """
        Validates that the state transitions in the block are consistent with the shard state.
        :param block: The block containing the state transitions.
        :return: True if the state transitions are valid, False otherwise.
        """
        temp_state = self.shard_state.copy()
        for transaction in block["transactions"]:
            if not self._apply_transaction_to_state(transaction, temp_state):
                return False
        return True

    def _apply_transaction_to_state(self, transaction, state):
        """
        Applies a transaction to a temporary state for validation.
        :param transaction: The transaction to apply.
        :param state: The temporary state to modify.
        :return: True if the transaction can be applied, False otherwise.
        """
        try:
            # Remove inputs from UTXO set
            for tx_input in transaction["inputs"]:
                del state["utxos"][(tx_input["tx_id"], tx_input["index"])]

            # Add outputs to UTXO set
            tx_id = transaction["tx_id"]
            for index, output in enumerate(transaction["outputs"]):
                state["utxos"][(tx_id, index)] = output

            return True
        except KeyError as e:
            print(f"UTXO not found during state transition: {e}")
            return False

    def _verify_signature(self, transaction):
        """
        Verifies the digital signature of a transaction.
        :param transaction: The transaction to verify.
        :return: True if the signature is valid, False otherwise.
        """
        # Placeholder for actual cryptographic signature verification
        return True


# Example usage
if __name__ == "__main__":
    shard_state = {
        "balances": {"Alice": 100, "Bob": 50},
        "utxos": {
            ("tx1", 0): {"receiver": "Alice", "amount": 50},
            ("tx1", 1): {"receiver": "Bob", "amount": 30}
        }
    }

    validator = ShardValidator(shard_id="shard_0", shard_state=shard_state)

    # Example block
    block = {
        "block_hash": "abc123",
        "previous_hash": "xyz789",
        "timestamp": int(time.time()),
        "transactions": [
            {
                "tx_id": "tx2",
                "sender": "Alice",
                "inputs": [{"tx_id": "tx1", "index": 0}],
                "outputs": [{"receiver": "Bob", "amount": 40}, {"receiver": "Alice", "amount": 9}],
                "nonce": 1,
                "fee": 1
            }
        ],
        "nonce": 42
    }

    # Validate the block
    is_valid = validator.validate_block(block)
    print("Block validation result:", is_valid)
