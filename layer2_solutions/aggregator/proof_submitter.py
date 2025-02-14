import hashlib
import time
from typing import Dict, Any


class ProofSubmitter:
    """Handles the submission of cryptographic proofs from Layer 2 to Layer 1."""

    def __init__(self):
        self.submitted_proofs = []  # List of submitted proofs
        self.pending_proofs = []  # Queue of proofs waiting for submission

    def generate_proof(self, batch_id: int, transactions: Dict[str, Any], state_root: str) -> Dict[str, Any]:
        """
        Generates a cryptographic proof for a batch of transactions.
        :param batch_id: The unique ID of the batch.
        :param transactions: The transactions included in the batch.
        :param state_root: The state root hash after processing the batch.
        :return: A dictionary containing the proof details.
        """
        proof_hash = hashlib.sha256(f"{batch_id}{transactions}{state_root}".encode()).hexdigest()
        proof = {
            "batch_id": batch_id,
            "transactions": transactions,
            "state_root": state_root,
            "proof_hash": proof_hash,
            "timestamp": time.time(),
        }
        self.pending_proofs.append(proof)
        print(f"Proof generated for batch {batch_id}: {proof_hash}")
        return proof

    def submit_proof(self) -> bool:
        """
        Submits the next pending proof to Layer 1.
        :return: True if a proof was submitted, False otherwise.
        """
        if not self.pending_proofs:
            print("No pending proofs to submit.")
            return False

        proof = self.pending_proofs.pop(0)
        self.submitted_proofs.append(proof)
        print(f"Proof for batch {proof['batch_id']} submitted to Layer 1: {proof['proof_hash']}")
        return True

    def list_submitted_proofs(self) -> Dict[int, str]:
        """
        Lists all submitted proofs.
        :return: A dictionary of batch IDs and their submitted proof hashes.
        """
        return {proof["batch_id"]: proof["proof_hash"] for proof in self.submitted_proofs}

    def list_pending_proofs(self) -> Dict[int, str]:
        """
        Lists all pending proofs.
        :return: A dictionary of batch IDs and their pending proof hashes.
        """
        return {proof["batch_id"]: proof["proof_hash"] for proof in self.pending_proofs}

    def verify_proof(self, proof_hash: str) -> bool:
        """
        Verifies if a submitted proof exists and is valid.
        :param proof_hash: The hash of the proof to verify.
        :return: True if the proof is valid, False otherwise.
        """
        for proof in self.submitted_proofs:
            if proof["proof_hash"] == proof_hash:
                print(f"Proof verified: {proof_hash}")
                return True
        print(f"Proof not found: {proof_hash}")
        return False


# Example usage
if __name__ == "__main__":
    submitter = ProofSubmitter()

    # Generate a proof
    batch_id = 1
    transactions = {"tx1": {"sender": "address1", "receiver": "address2", "amount": 50.0}}
    state_root = "abc123statehash"
    proof = submitter.generate_proof(batch_id, transactions, state_root)

    # Submit the proof
    submitter.submit_proof()

    # List submitted proofs
    print("\nSubmitted Proofs:")
    print(submitter.list_submitted_proofs())

    # List pending proofs
    print("\nPending Proofs:")
    print(submitter.list_pending_proofs())

    # Verify a proof
    submitter.verify_proof(proof["proof_hash"])
