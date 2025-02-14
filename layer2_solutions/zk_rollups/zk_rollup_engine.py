import hashlib
import json
from typing import List, Dict, Any
from zk_proof_generator import ZKProofGenerator
from rollup_verifier import RollupVerifier

class ZKRollupEngine:
    """Core logic for aggregating transactions and managing zk-rollups."""

    def __init__(self, batch_size: int, rollup_contract_address: str):
        """
        Initializes the ZKRollupEngine.
        :param batch_size: Maximum number of transactions per rollup batch.
        :param rollup_contract_address: Address of the Layer 1 rollup smart contract.
        """
        self.batch_size = batch_size
        self.rollup_contract_address = rollup_contract_address
        self.pending_transactions = []
        self.processed_batches = []

    def add_transaction(self, transaction: Dict[str, Any]):
        """
        Adds a transaction to the pending queue.
        :param transaction: The transaction data (e.g., sender, receiver, amount).
        """
        if len(self.pending_transactions) >= self.batch_size:
            print("Batch size reached. Consider submitting the rollup.")
            return
        self.pending_transactions.append(transaction)
        print(f"Transaction added. Pending transactions: {len(self.pending_transactions)}")

    def aggregate_transactions(self) -> str:
        """
        Aggregates the pending transactions into a batch and generates a rollup.
        :return: The batch hash as a unique identifier.
        """
        if not self.pending_transactions:
            raise ValueError("No pending transactions to aggregate.")

        batch_data = json.dumps(self.pending_transactions, sort_keys=True)
        batch_hash = hashlib.sha256(batch_data.encode()).hexdigest()

        self.processed_batches.append({
            "batch_hash": batch_hash,
            "transactions": self.pending_transactions,
        })

        self.pending_transactions = []  # Clear pending transactions after aggregation
        print(f"Batch aggregated with hash: {batch_hash}")
        return batch_hash

    def generate_proof(self, batch_hash: str) -> Dict[str, Any]:
        """
        Generates a zk-proof for the aggregated batch.
        :param batch_hash: Hash of the aggregated batch.
        :return: The zk-proof data.
        """
        batch = next((b for b in self.processed_batches if b["batch_hash"] == batch_hash), None)
        if not batch:
            raise ValueError("Batch not found.")

        proof = ZKProofGenerator.generate(batch["transactions"])
        print(f"Proof generated for batch: {batch_hash}")
        return {"batch_hash": batch_hash, "proof": proof}

    def submit_rollup(self, batch_hash: str, proof: Dict[str, Any]) -> bool:
        """
        Submits the rollup batch and proof to the Layer 1 contract.
        :param batch_hash: Hash of the aggregated batch.
        :param proof: The zk-proof data for the batch.
        :return: True if submission is successful, False otherwise.
        """
        if not RollupVerifier.verify(proof, batch_hash):
            print("Proof verification failed.")
            return False

        print(f"Rollup batch {batch_hash} successfully submitted to contract {self.rollup_contract_address}.")
        return True


# Example usage
if __name__ == "__main__":
    # Initialize zk-rollup engine
    zk_engine = ZKRollupEngine(batch_size=5, rollup_contract_address="0xRollupContract")

    # Add transactions
    zk_engine.add_transaction({"sender": "address1", "receiver": "address2", "amount": 50})
    zk_engine.add_transaction({"sender": "address3", "receiver": "address4", "amount": 100})

    # Aggregate transactions into a batch
    batch_hash = zk_engine.aggregate_transactions()

    # Generate zk-proof for the batch
    proof = zk_engine.generate_proof(batch_hash)

    # Submit the rollup to Layer 1
    zk_engine.submit_rollup(batch_hash, proof)
