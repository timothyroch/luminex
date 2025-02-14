import time
from blocks.blockchain_state import Blockchain
from blocks.block import Block

class ConsensusEngine:
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain

    def proof_of_work(self, transactions: list, difficulty: int) -> Block:
        """Implements Proof of Work by mining a new block."""
        last_block = self.blockchain.get_latest_block()
        new_block = Block(last_block.index + 1, last_block.hash, transactions)
        print("Mining new block...")
        new_block.mine_block(difficulty)
        return new_block

    def validate_and_add_block(self, block: Block, difficulty: int) -> bool:
        """Validates and adds a new block to the blockchain."""
        if self.blockchain.add_block(block, difficulty):
            print(f"Block #{block.index} added to the chain.")
            return True
        else:
            print("Block validation failed.")
            return False

    def resolve_forks(self, peer_chains: list, difficulty: int):
        """Compares peer chains and resolves forks by adopting the longest valid chain."""
        for peer_chain in peer_chains:
            if self.blockchain.resolve_fork(peer_chain, difficulty):
                print("Fork resolved. Adopted the longer chain.")
                return

    def validate_chain(self, difficulty: int) -> bool:
        """Validates the entire blockchain."""
        return self.blockchain.is_chain_valid(difficulty)

    def mine_and_add_block(self, transactions: list, difficulty: int):
        """Handles the full process of mining and adding a block."""
        new_block = self.proof_of_work(transactions, difficulty)
        if self.validate_and_add_block(new_block, difficulty):
            print("Block mined and added successfully.")
        else:
            print("Block mining or validation failed.")

    def synchronize_with_peers(self, peer_blocks: list):
        """Synchronizes blocks with peers (simplified version)."""
        for block in peer_blocks:
            if self.validate_and_add_block(block, difficulty=2):
                print(f"Synchronized block #{block.index}.")
            else:
                print(f"Failed to synchronize block #{block.index}.")

# Example usage
if __name__ == "__main__":
    blockchain = Blockchain()
    consensus_engine = ConsensusEngine(blockchain)
    difficulty = 2

    # Mine and add a block
    transactions = [{"sender": "Alice", "receiver": "Bob", "amount": 10}]
    consensus_engine.mine_and_add_block(transactions, difficulty)

    # Validate the chain
    print("Is blockchain valid?", consensus_engine.validate_chain(difficulty))
