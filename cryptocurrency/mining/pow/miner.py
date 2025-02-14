import time
from blocks.block import Block # type: ignore
from transactions.transaction import TransactionPool # type: ignore
from blocks.blockchain_state import Blockchain


class Miner:
    def __init__(self, blockchain: Blockchain, transaction_pool: TransactionPool, miner_address: str, reward: float):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool
        self.miner_address = miner_address
        self.reward = reward
        self.is_mining = False

    def create_coinbase_transaction(self):
        """Creates a coinbase transaction for the miner's reward."""
        return {"sender": "COINBASE", "receiver": self.miner_address, "amount": self.reward}

    def mine_block(self, difficulty: int):
        """Fetches transactions, mines a new block, and adds it to the blockchain."""
        pending_transactions = self.transaction_pool.get_pending_transactions(max_count=10)
        coinbase_tx = self.create_coinbase_transaction()
        transactions = [coinbase_tx] + [tx.to_dict() for tx in pending_transactions]

        # Create a new block
        latest_block = self.blockchain.get_latest_block()
        new_block = Block(index=latest_block.index + 1, previous_hash=latest_block.hash, transactions=transactions)

        print(f"Mining new block #{new_block.index}...")
        start_time = time.time()

        # Perform Proof of Work
        new_block.mine_block(difficulty)
        end_time = time.time()

        # Add the block to the chain if valid
        if self.blockchain.add_block(new_block, difficulty):
            print(f"Block #{new_block.index} mined successfully in {end_time - start_time:.2f} seconds.")
            # Remove confirmed transactions from the pool
            confirmed_tx_hashes = [tx["hash"] for tx in transactions if "hash" in tx]
            self.transaction_pool.remove_confirmed_transactions(confirmed_tx_hashes)
        else:
            print("Failed to add the mined block. Validation error.")

    def start_mining(self, difficulty: int):
        """Starts the mining process in a loop."""
        self.is_mining = True
        print("Mining started...")
        while self.is_mining:
            self.mine_block(difficulty)
            time.sleep(1)  # Prevents excessive CPU usage; adjust as needed.

    def stop_mining(self):
        """Stops the mining process."""
        self.is_mining = False
        print("Mining stopped.")


# Example usage
if __name__ == "__main__":
    from transactions.transaction_pool import TransactionPool # type: ignore

    # Set up blockchain, transaction pool, and miner
    blockchain = Blockchain()
    transaction_pool = TransactionPool()
    miner_address = "Miner1Address"
    miner = Miner(blockchain, transaction_pool, miner_address, reward=50)

    # Add some dummy transactions to the pool
    transaction_pool.add_transaction({"sender": "Alice", "receiver": "Bob", "amount": 10}, sender_balance=100)
    transaction_pool.add_transaction({"sender": "Charlie", "receiver": "Dave", "amount": 20}, sender_balance=50)

    # Start mining
    difficulty = 2
    miner.start_mining(difficulty)
