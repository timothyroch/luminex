import time
import random
from transactions.transaction_pool import TransactionPool
from blocks.blockchain_state import Blockchain
from blocks.block import Block

def generate_random_transaction():
    """Generates a random transaction for testing."""
    return {
        "sender": f"User{random.randint(1, 1000)}",
        "receiver": f"User{random.randint(1, 1000)}",
        "amount": random.uniform(1, 100)
    }

def measure_tps(transaction_pool, blockchain, num_transactions, block_size, difficulty):
    """
    Measures transactions per second (TPS) under specified load.
    :param transaction_pool: TransactionPool instance.
    :param blockchain: Blockchain instance.
    :param num_transactions: Total number of transactions to test.
    :param block_size: Maximum number of transactions per block.
    :param difficulty: Mining difficulty.
    :return: TPS value.
    """
    # Generate transactions and add them to the pool
    for _ in range(num_transactions):
        transaction_pool.add_transaction(generate_random_transaction(), sender_balance=1000)

    # Start the TPS measurement
    start_time = time.time()
    while len(transaction_pool.transactions) > 0:
        # Get a batch of transactions
        pending_transactions = transaction_pool.get_pending_transactions(max_count=block_size)
        
        # Create a new block
        latest_block = blockchain.get_latest_block()
        new_block = Block(latest_block.index + 1, latest_block.hash, [tx.to_dict() for tx in pending_transactions])
        
        # Mine the block
        new_block.mine_block(difficulty)
        blockchain.add_block(new_block, difficulty)
        
        # Remove confirmed transactions from the pool
        confirmed_tx_hashes = [tx["hash"] for tx in new_block.transactions if "hash" in tx]
        transaction_pool.remove_confirmed_transactions(confirmed_tx_hashes)

    # End TPS measurement
    end_time = time.time()
    elapsed_time = end_time - start_time
    tps = num_transactions / elapsed_time

    return tps

if __name__ == "__main__":
    blockchain = Blockchain()
    transaction_pool = TransactionPool()
    difficulty = 2
    block_size = 10  # Maximum transactions per block
    num_transactions = 1000  # Total transactions to test

    print(f"Testing TPS with {num_transactions} transactions and block size of {block_size}...")
    tps = measure_tps(transaction_pool, blockchain, num_transactions, block_size, difficulty)
    print(f"Transactions per second (TPS): {tps:.2f}")
