from blocks.block import Block
from typing import List

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Creates the genesis block (first block in the blockchain)."""
        genesis_block = Block(0, "0" * 64, [])
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """Returns the latest block in the chain."""
        return self.chain[-1]

    def add_block(self, new_block: Block, difficulty: int) -> bool:
        """Adds a new block to the chain after validation."""
        if self.is_valid_new_block(new_block, self.get_latest_block(), difficulty):
            self.chain.append(new_block)
            return True
        return False

    def is_valid_new_block(self, new_block: Block, previous_block: Block, difficulty: int) -> bool:
        """Validates the new block before adding it to the chain."""
        if new_block.previous_hash != previous_block.hash:
            print("Invalid previous hash.")
            return False
        if not new_block.hash.startswith("0" * difficulty):
            print("Block does not meet difficulty target.")
            return False
        if new_block.hash != new_block.calculate_hash():
            print("Invalid block hash.")
            return False
        return True

    def is_chain_valid(self, difficulty: int) -> bool:
        """Validates the entire chain."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if not self.is_valid_new_block(current_block, previous_block, difficulty):
                return False
        return True

    def resolve_fork(self, new_chain: List[Block], difficulty: int) -> bool:
        """Replaces the current chain with a longer valid chain, if found."""
        if len(new_chain) > len(self.chain) and self.is_valid_chain(new_chain, difficulty):
            self.chain = new_chain
            print("Chain replaced with a longer valid chain.")
            return True
        return False

    def is_valid_chain(self, chain: List[Block], difficulty: int) -> bool:
        """Checks if a given chain is valid."""
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]
            if not self.is_valid_new_block(current_block, previous_block, difficulty):
                return False
        return True

    def __str__(self) -> str:
        """Returns a string representation of the blockchain."""
        return "\n".join(str(block) for block in self.chain)


# Example usage
if __name__ == "__main__":
    from blocks.block import Block

    blockchain = Blockchain()
    difficulty = 2

    # Add a new block
    transactions = [{"sender": "Alice", "receiver": "Bob", "amount": 10}]
    new_block = Block(blockchain.get_latest_block().index + 1, blockchain.get_latest_block().hash, transactions)
    new_block.mine_block(difficulty)
    blockchain.add_block(new_block, difficulty)

    # Print the blockchain
    print(blockchain)
