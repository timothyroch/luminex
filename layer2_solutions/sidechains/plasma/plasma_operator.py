import hashlib
import time
from typing import List, Dict, Any


class PlasmaOperator:
    """Handles transaction aggregation, block creation, and Plasma commitments."""

    def __init__(self, plasma_contract_address: str, block_interval_seconds: int):
        """
        Initializes the PlasmaOperator.
        :param plasma_contract_address: Address of the Layer 1 Plasma contract.
        :param block_interval_seconds: Time interval (in seconds) for creating new blocks.
        """
        self.plasma_contract_address = plasma_contract_address
        self.block_interval_seconds = block_interval_seconds
        self.pending_transactions = []
        self.blocks = []
        self.last_block_time = time.time()

    def add_transaction(self, transaction: Dict[str, Any]):
        """
        Adds a new transaction to the pool.
        :param transaction: The transaction data (e.g., sender, receiver, amount).
        """
        self.pending_transactions.append(transaction)
        print(f"Transaction added. Pending transactions: {len(self.pending_transactions)}")

    def create_block(self):
        """
        Creates a new Plasma block from pending transactions.
        """
        if not self.pending_transactions:
            print("No pending transactions to create a block.")
            return

        if time.time() - self.last_block_time < self.block_interval_seconds:
            print("Block interval not reached yet.")
            return

        # Aggregate transactions into a block
        block_data = {
            "block_number": len(self.blocks) + 1,
            "transactions": self.pending_transactions,
            "timestamp": time.time()
        }
        block_hash = self._calculate_block_hash(block_data)
        block_data["block_hash"] = block_hash

        self.blocks.append(block_data)
        self.pending_transactions = []  # Clear pending transactions
        self.last_block_time = time.time()

        print(f"Block {block_data['block_number']} created with hash: {block_hash}")

    def submit_commitment(self):
        """
        Submits the latest block's commitment to the Plasma contract.
        """
        if not self.blocks:
            print("No blocks available to submit.")
            return

        latest_block = self.blocks[-1]
        block_hash = latest_block["block_hash"]
        # Simulate commitment submission to Layer 1
        print(f"Submitting block {latest_block['block_number']} with hash {block_hash} to Plasma contract {self.plasma_contract_address}.")

    def _calculate_block_hash(self, block_data: Dict[str, Any]) -> str:
        """
        Calculates a unique hash for the given block data.
        :param block_data: The block data.
        :return: The hash of the block.
        """
        block_string = f"{block_data['block_number']}{block_data['transactions']}{block_data['timestamp']}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def list_blocks(self) -> List[Dict[str, Any]]:
        """
        Lists all created blocks.
        :return: A list of block data.
        """
        return self.blocks


# Example usage
if __name__ == "__main__":
    plasma_operator = PlasmaOperator(plasma_contract_address="0xPlasmaContract", block_interval_seconds=60)

    # Add transactions
    plasma_operator.add_transaction({"sender": "address1", "receiver": "address2", "amount": 50})
    plasma_operator.add_transaction({"sender": "address3", "receiver": "address4", "amount": 100})

    # Create a block
    plasma_operator.create_block()

    # Submit the block's commitment
    plasma_operator.submit_commitment()

    # List all created blocks
    print("\nAll Blocks:")
    for block in plasma_operator.list_blocks():
        print(block)
