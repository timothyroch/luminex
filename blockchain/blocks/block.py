import hashlib
import time
from typing import List, Dict
import json


class Block:
    def __init__(self, index: int, previous_hash: str, transactions: List[Dict], nonce: int = 0):
        self.index = index
        self.timestamp = int(time.time())
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()
        self.merkle_root = self.calculate_merkle_root()

    def calculate_hash(self) -> str:
        """Calculates the hash of the block."""
        block_content = f"{self.index}{self.timestamp}{self.previous_hash}{self.merkle_root}{self.nonce}"
        return hashlib.sha256(block_content.encode()).hexdigest()

    def calculate_merkle_root(self) -> str:
        """Calculates the Merkle root of the block's transactions."""
        hashes = [hashlib.sha256(json.dumps(tx).encode()).hexdigest() for tx in self.transactions]
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])
            hashes = [hashlib.sha256((hashes[i] + hashes[i + 1]).encode()).hexdigest()
                      for i in range(0, len(hashes), 2)]
        return hashes[0] if hashes else ""

    def mine_block(self, difficulty: int):
        """Simple mining algorithm for Proof of Work."""
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

    def to_dict(self) -> dict:
        """Serializes the block to a dictionary."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "transactions": self.transactions,
            "nonce": self.nonce,
            "hash": self.hash,
            "merkle_root": self.merkle_root
        }

    @staticmethod
    def from_dict(data: dict) -> 'Block':
        """Deserializes a dictionary into a Block object."""
        return Block(
            index=data["index"],
            previous_hash=data["previous_hash"],
            transactions=data["transactions"],
            nonce=data["nonce"]
        )

    def is_valid(self, difficulty: int) -> bool:
        """Validates the block's integrity."""
        return (self.hash == self.calculate_hash() and
                self.hash.startswith('0' * difficulty))


# Example usage:
if __name__ == "__main__":
    transactions = [{"sender": "Alice", "receiver": "Bob", "amount": 10}]
    block = Block(1, "0" * 64, transactions)
    print(block)
    block.mine_block(2)
    print(f"Mined Block: {block.hash}")
