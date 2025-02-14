import hashlib
import time
import heapq
import json

class MempoolManager:
    """Manages the mempool of unconfirmed transactions."""

    def __init__(self, config_path="blockchain/transactions/mempool/mempool_config.json"):
        """
        Initializes the MempoolManager with configuration settings.
        :param config_path: Path to the mempool configuration file.
        """
        with open(config_path, "r") as file:
            self.config = json.load(file)

        self.mempool = []  # A heap to store transactions, sorted by priority
        self.transaction_set = set()  # For quick duplicate detection
        self.max_transactions = self.config["max_transactions"]
        self.min_fee = self.config["min_fee"]
        self.expiration_time = self.config["transaction_expiration_seconds"]

    def add_transaction(self, transaction):
        """
        Adds a transaction to the mempool if it is valid and meets fee requirements.
        :param transaction: A dictionary containing transaction details.
        :return: True if the transaction was added, False otherwise.
        """
        transaction_id = self._get_transaction_id(transaction)
        current_time = time.time()

        if transaction_id in self.transaction_set:
            print("Transaction already in mempool.")
            return False

        if transaction["fee"] < self.min_fee:
            print("Transaction fee below minimum threshold.")
            return False

        if len(self.mempool) >= self.max_transactions:
            print("Mempool is full.")
            return False

        # Attach timestamp for expiration management
        transaction["timestamp"] = current_time

        # Calculate priority (fee per byte) for prioritization
        priority = transaction["fee"] / max(len(json.dumps(transaction)), 1)
        heapq.heappush(self.mempool, (-priority, transaction))  # Use negative for max-heap behavior
        self.transaction_set.add(transaction_id)

        print(f"Transaction {transaction_id} added to mempool.")
        return True

    def remove_confirmed_transactions(self, confirmed_transactions):
        """
        Removes transactions from the mempool that have been included in a block.
        :param confirmed_transactions: A list of confirmed transaction IDs.
        """
        updated_mempool = []
        for priority, transaction in self.mempool:
            if self._get_transaction_id(transaction) not in confirmed_transactions:
                updated_mempool.append((priority, transaction))

        # Rebuild the heap
        self.mempool = updated_mempool
        heapq.heapify(self.mempool)

        # Update the transaction set
        self.transaction_set = {self._get_transaction_id(tx[1]) for tx in self.mempool}
        print(f"Removed {len(confirmed_transactions)} confirmed transactions from mempool.")

    def cleanup_expired_transactions(self):
        """
        Removes transactions that have been in the mempool longer than the expiration time.
        """
        current_time = time.time()
        updated_mempool = []
        removed_count = 0

        for priority, transaction in self.mempool:
            if current_time - transaction["timestamp"] <= self.expiration_time:
                updated_mempool.append((priority, transaction))
            else:
                removed_count += 1
                self.transaction_set.remove(self._get_transaction_id(transaction))

        self.mempool = updated_mempool
        heapq.heapify(self.mempool)
        print(f"Removed {removed_count} expired transactions from mempool.")

    def get_transactions(self, limit=None):
        """
        Retrieves a list of transactions from the mempool, ordered by priority.
        :param limit: Optional limit on the number of transactions to retrieve.
        :return: A list of transactions.
        """
        sorted_transactions = [tx[1] for tx in sorted(self.mempool, reverse=True)]
        return sorted_transactions[:limit] if limit else sorted_transactions

    def _get_transaction_id(self, transaction):
        """
        Computes a unique ID for a transaction.
        :param transaction: A dictionary representing the transaction.
        :return: A string hash representing the transaction ID.
        """
        transaction_data = json.dumps(transaction, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(transaction_data.encode('utf-8')).hexdigest()


# Example usage
if __name__ == "__main__":
    mempool_manager = MempoolManager()

    # Example transactions
    transactions = [
        {"sender": "Alice", "receiver": "Bob", "amount": 50, "fee": 0.01},
        {"sender": "Charlie", "receiver": "Dave", "amount": 20, "fee": 0.005},
        {"sender": "Eve", "receiver": "Frank", "amount": 30, "fee": 0.02},
    ]

    # Add transactions to mempool
    for tx in transactions:
        mempool_manager.add_transaction(tx)

    # Display transactions in the mempool
    print("Current Mempool:", mempool_manager.get_transactions())

    # Simulate block confirmation
    confirmed_tx_ids = [mempool_manager._get_transaction_id(transactions[0])]
    mempool_manager.remove_confirmed_transactions(confirmed_tx_ids)

    # Clean up expired transactions
    mempool_manager.cleanup_expired_transactions()

    # Display updated mempool
    print("Updated Mempool:", mempool_manager.get_transactions())
