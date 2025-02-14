import hashlib

class MerkleTree:
    """Represents a Merkle Tree and provides tools for generating and verifying Merkle proofs."""

    def __init__(self, transactions):
        """
        Initializes the Merkle Tree with a list of transactions.
        :param transactions: A list of transactions (strings or bytes).
        """
        self.leaves = [self._hash(tx) for tx in transactions]
        self.root = self._build_merkle_tree(self.leaves)

    def _hash(self, data):
        """
        Computes the SHA-256 hash of the given data.
        :param data: The input data (string or bytes).
        :return: The SHA-256 hash as a hexadecimal string.
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()

    def _build_merkle_tree(self, leaves):
        """
        Builds the Merkle Tree and computes the Merkle Root.
        :param leaves: A list of hashed leaf nodes.
        :return: The Merkle Root as a hexadecimal string.
        """
        while len(leaves) > 1:
            if len(leaves) % 2 != 0:  # Duplicate the last hash if odd number of leaves
                leaves.append(leaves[-1])
            new_level = []
            for i in range(0, len(leaves), 2):
                combined_hash = self._hash(leaves[i] + leaves[i + 1])
                new_level.append(combined_hash)
            leaves = new_level
        return leaves[0]

    def get_proof(self, transaction):
        """
        Generates a Merkle proof for a given transaction.
        :param transaction: The transaction to prove.
        :return: A list of proof nodes and the transaction's index.
        """
        if isinstance(transaction, str):
            transaction = transaction.encode('utf-8')
        transaction_hash = self._hash(transaction)

        if transaction_hash not in self.leaves:
            raise ValueError("Transaction not found in the Merkle Tree.")

        index = self.leaves.index(transaction_hash)
        proof = []
        current_level = self.leaves

        while len(current_level) > 1:
            if len(current_level) % 2 != 0:  # Duplicate the last hash if odd number of leaves
                current_level.append(current_level[-1])

            pair_index = index ^ 1  # Sibling index
            proof.append(current_level[pair_index])

            # Move to the next level
            index //= 2
            new_level = []
            for i in range(0, len(current_level), 2):
                combined_hash = self._hash(current_level[i] + current_level[i + 1])
                new_level.append(combined_hash)
            current_level = new_level

        return proof

    @staticmethod
    def verify_proof(transaction, proof, root):
        """
        Verifies a Merkle proof.
        :param transaction: The original transaction.
        :param proof: The Merkle proof as a list of sibling hashes.
        :param root: The Merkle root to verify against.
        :return: True if the proof is valid, False otherwise.
        """
        if isinstance(transaction, str):
            transaction = transaction.encode('utf-8')
        current_hash = hashlib.sha256(transaction).hexdigest()

        for sibling_hash in proof:
            if current_hash < sibling_hash:
                current_hash = hashlib.sha256((current_hash + sibling_hash).encode('utf-8')).hexdigest()
            else:
                current_hash = hashlib.sha256((sibling_hash + current_hash).encode('utf-8')).hexdigest()

        return current_hash == root


# Example usage
if __name__ == "__main__":
    # List of transactions
    transactions = ["tx1", "tx2", "tx3", "tx4"]

    # Create Merkle Tree
    merkle_tree = MerkleTree(transactions)
    print("Merkle Root:", merkle_tree.root)

    # Generate a proof for a specific transaction
    transaction = "tx2"
    proof = merkle_tree.get_proof(transaction)
    print(f"Merkle Proof for {transaction}:", proof)

    # Verify the proof
    is_valid = MerkleTree.verify_proof(transaction, proof, merkle_tree.root)
    print(f"Proof Valid for {transaction}: {is_valid}")

    # Verify with a tampered transaction (should fail)
    tampered_transaction = "tx2_tampered"
    is_valid = MerkleTree.verify_proof(tampered_transaction, proof, merkle_tree.root)
    print(f"Proof Valid for Tampered Transaction: {is_valid}")
