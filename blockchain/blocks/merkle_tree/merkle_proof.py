import hashlib
import json

class MerkleProof:
    """Implements Merkle proof generation and verification."""

    @staticmethod
    def _hash_data(data):
        """
        Computes the SHA-256 hash of the given data.
        :param data: The data to hash (string or JSON serializable).
        :return: A hexadecimal SHA-256 hash.
        """
        if not isinstance(data, str):
            data = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    @staticmethod
    def generate_proof(transactions, target_transaction):
        """
        Generates a Merkle proof for a target transaction.
        :param transactions: The list of transactions.
        :param target_transaction: The transaction to generate the proof for.
        :return: A tuple (proof, index) where proof is a list of hashes and index is the position of the target.
        """
        if target_transaction not in transactions:
            raise ValueError("Target transaction not found in the list of transactions.")

        # Hash all transactions
        hashed_transactions = [MerkleProof._hash_data(tx) for tx in transactions]

        # Determine the index of the target transaction
        target_index = transactions.index(target_transaction)

        # Generate proof
        proof = []
        current_level = hashed_transactions
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left

                # If target is in this pair, record the sibling hash for the proof
                if i == target_index or (i + 1) == target_index:
                    sibling_hash = right if i == target_index else left
                    proof.append(sibling_hash)

                # Compute parent node
                next_level.append(MerkleProof._hash_data(left + right))

            # Move to the next level
            current_level = next_level
            target_index //= 2

        return proof, transactions.index(target_transaction)

    @staticmethod
    def verify_proof(merkle_root, target_transaction, proof, index):
        """
        Verifies a Merkle proof.
        :param merkle_root: The Merkle root of the tree.
        :param target_transaction: The transaction being verified.
        :param proof: The proof (list of sibling hashes).
        :param index: The position of the transaction in the original list.
        :return: True if the proof is valid, False otherwise.
        """
        current_hash = MerkleProof._hash_data(target_transaction)

        # Recompute the Merkle root using the proof
        for sibling_hash in proof:
            if index % 2 == 0:  # Left child
                current_hash = MerkleProof._hash_data(current_hash + sibling_hash)
            else:  # Right child
                current_hash = MerkleProof._hash_data(sibling_hash + current_hash)
            index //= 2

        # Check if the recomputed root matches the provided root
        return current_hash == merkle_root


# Example usage
if __name__ == "__main__":
    # Sample transactions
    transactions = [
        {"sender": "Alice", "receiver": "Bob", "amount": 50},
        {"sender": "Charlie", "receiver": "Dave", "amount": 20},
        {"sender": "Eve", "receiver": "Frank", "amount": 30},
        {"sender": "Grace", "receiver": "Hank", "amount": 40}
    ]

    # Target transaction
    target_transaction = {"sender": "Charlie", "receiver": "Dave", "amount": 20}

    # Generate Merkle proof
    from blockchain.blocks.merkle_tree import MerkleTree
    merkle_tree = MerkleTree(transactions)
    merkle_root = merkle_tree.get_merkle_root()

    proof, index = MerkleProof.generate_proof(transactions, target_transaction)
    print("Merkle Root:", merkle_root)
    print("Proof:", proof)
    print("Index:", index)

    # Verify Merkle proof
    is_valid = MerkleProof.verify_proof(merkle_root, target_transaction, proof, index)
    print("Proof is valid:", is_valid)
