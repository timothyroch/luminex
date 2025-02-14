import hashlib

class Hashing:
    """Provides cryptographic hash functions for the blockchain."""

    @staticmethod
    def sha256(data):
        """
        Computes the SHA-256 hash of the given data.
        :param data: The input data (string or bytes).
        :return: The SHA-256 hash as a hexadecimal string.
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def keccak256(data):
        """
        Computes the Keccak-256 hash of the given data.
        :param data: The input data (string or bytes).
        :return: The Keccak-256 hash as a hexadecimal string.
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.new('sha3_256', data).hexdigest()

    @staticmethod
    def double_sha256(data):
        """
        Computes the double SHA-256 hash (SHA-256 applied twice) of the given data.
        :param data: The input data (string or bytes).
        :return: The double SHA-256 hash as a hexadecimal string.
        """
        return Hashing.sha256(Hashing.sha256(data))

    @staticmethod
    def ripemd160(data):
        """
        Computes the RIPEMD-160 hash of the given data.
        :param data: The input data (string or bytes).
        :return: The RIPEMD-160 hash as a hexadecimal string.
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(data)
        return ripemd160.hexdigest()

    @staticmethod
    def hash160(data):
        """
        Computes the HASH160 of the given data (RIPEMD-160 applied to the SHA-256 hash).
        :param data: The input data (string or bytes).
        :return: The HASH160 as a hexadecimal string.
        """
        return Hashing.ripemd160(Hashing.sha256(data))

    @staticmethod
    def merkle_root(hashes):
        """
        Computes the Merkle root from a list of transaction hashes.
        :param hashes: A list of transaction hashes (hexadecimal strings).
        :return: The Merkle root as a hexadecimal string.
        """
        if not hashes:
            return None
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:  # Duplicate the last hash if odd number of hashes
                hashes.append(hashes[-1])
            new_level = []
            for i in range(0, len(hashes), 2):
                concatenated_hash = Hashing.double_sha256(hashes[i] + hashes[i + 1])
                new_level.append(concatenated_hash)
            hashes = new_level
        return hashes[0]


# Example usage
if __name__ == "__main__":
    data = "Hello, Blockchain!"

    # SHA-256 hash
    print("SHA-256:", Hashing.sha256(data))

    # Keccak-256 hash
    print("Keccak-256:", Hashing.keccak256(data))

    # Double SHA-256 hash
    print("Double SHA-256:", Hashing.double_sha256(data))

    # RIPEMD-160 hash
    print("RIPEMD-160:", Hashing.ripemd160(data))

    # HASH160
    print("HASH160:", Hashing.hash160(data))

    # Merkle root from sample transaction hashes
    sample_hashes = [
        Hashing.sha256("tx1"),
        Hashing.sha256("tx2"),
        Hashing.sha256("tx3"),
        Hashing.sha256("tx4")
    ]
    print("Merkle Root:", Hashing.merkle_root(sample_hashes))
