import hashlib


class HashingAlgorithm:
    """Implements cryptographic hashing functions for the blockchain."""

    @staticmethod
    def sha256(data: str) -> str:
        """
        Computes the SHA-256 hash of the input data.
        :param data: The input data as a string.
        :return: The hexadecimal SHA-256 hash.
        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    @staticmethod
    def double_sha256(data: str) -> str:
        """
        Computes the double SHA-256 hash of the input data.
        :param data: The input data as a string.
        :return: The hexadecimal double SHA-256 hash.
        """
        first_hash = hashlib.sha256(data.encode('utf-8')).digest()
        return hashlib.sha256(first_hash).hexdigest()

    @staticmethod
    def merkle_hash(left_hash: str, right_hash: str) -> str:
        """
        Computes the hash of two concatenated hashes (used in Merkle trees).
        :param left_hash: The left hash as a hexadecimal string.
        :param right_hash: The right hash as a hexadecimal string.
        :return: The hexadecimal hash of the concatenated hashes.
        """
        combined = left_hash + right_hash
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()

    @staticmethod
    def is_valid_hash(hash_value: str, difficulty: int) -> bool:
        """
        Checks if a hash satisfies the difficulty level.
        :param hash_value: The hash value as a hexadecimal string.
        :param difficulty: The number of leading zeroes required.
        :return: True if the hash meets the difficulty requirement, False otherwise.
        """
        target = '0' * difficulty
        return hash_value.startswith(target)


# Example usage
if __name__ == "__main__":
    data = "Blockchain Example"
    difficulty = 4

    print("SHA-256 Hash:", HashingAlgorithm.sha256(data))
    print("Double SHA-256 Hash:", HashingAlgorithm.double_sha256(data))

    left_hash = HashingAlgorithm.sha256("Transaction 1")
    right_hash = HashingAlgorithm.sha256("Transaction 2")
    print("Merkle Hash:", HashingAlgorithm.merkle_hash(left_hash, right_hash))

    # Proof of Work Simulation
    nonce = 0
    while True:
        hash_value = HashingAlgorithm.sha256(data + str(nonce))
        if HashingAlgorithm.is_valid_hash(hash_value, difficulty):
            print(f"Valid hash found: {hash_value} with nonce {nonce}")
            break
        nonce += 1
