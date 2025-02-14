import hashlib
import json

class MerkleTree:
    """Implements a Merkle tree for hashing and verifying transactions."""

    def __init__(self, transactions):
        """
        Initializes the MerkleTree.
        :param transactions: A list of transactions to include in the Merkle tree.
        """
        self.transactions = transactions
        self.merkle_root = None
        self.tree = []
        self.build_tree()

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

    def build_tree(self):
        """
        Builds the Merkle tree from the list of transactions.
        """
        if not self.transactions:
            raise ValueError("No transactions provided to build the Merkle tree.")

        # Hash each transaction
        current_level = [self._hash_data(tx) for tx in self.transactions]
        self.tree.append(current_level)

        # Build the tree level by level
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                # Pair up adjacent hashes; if odd, duplicate the last hash
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                next_level.append(self._hash_data(left + right))
            self.tree.append(next_level)
            current_level = next_level

        # The root of the tree is the last remaining hash
        self.merkle_root = self.tree[-1][0]

    def get_merkle_root(self):
        """
        Returns the Merkle root.
        :return: The Merkle root.
        """
        return self.merkle_root

    def get_tree(self):
        """
        Returns the entire Merkle tree as a list of levels.
        :return: The Merkle tree.
        """
        return self.tree


# Example usage
if __name__ == "__main__":
    # Sample transactions
    transactions = [
        {"sender": "Alice", "receiver": "Bob", "amount": 50},
        {"sender": "Charlie", "receiver": "Dave", "amount": 20},
        {"sender": "Eve", "receiver": "Frank", "amount": 30},
        {"sender": "Grace", "receiver": "Hank", "amount": 40}
    ]

    # Build the Merkle tree
    merkle_tree = MerkleTree(transactions)
    print("Merkle Root:", merkle_tree.get_merkle_root())
    print("Merkle Tree Levels:")
    for level in merkle_tree.get_tree():
        print(level)
