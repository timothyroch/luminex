from typing import List, Dict
from transactions.transaction import Transaction
from threading import Lock


class TransactionPool:
    def __init__(self, max_pool_size: int = 1000):
        """Initializes the transaction pool."""
        self.transactions: Dict[str, Transaction] = {}  # Use transaction hash as key for uniqueness
        self.lock = Lock()  # Thread safety for concurrent access
        self.max_pool_size = max_pool_size  # Cap the number of transactions

    def add_transaction(self, transaction: Transaction, sender_balance: float) -> bool:
        """
        Adds a transaction to the pool after validation.
        :param transaction: The Transaction object to add.
        :param sender_balance: The current balance of the sender.
        :return: True if the transaction was added, False otherwise.
        """
        with self.lock:  # Ensure thread-safe operation
            if len(self.transactions) >= self.max_pool_size:
                print("Transaction pool is full. Discarding transaction.")
                return False

            if not self.is_valid_transaction(transaction, sender_balance):
                print("Invalid transaction. Discarded.")
                return False

            tx_hash = transaction.calculate_hash()
            if tx_hash in self.transactions:
                print("Duplicate transaction. Discarded.")
                return False

            self.transactions[tx_hash] = transaction
            print(f"Transaction from {transaction.sender} to {transaction.receiver} added.")
            return True

    def is_valid_transaction(self, transaction: Transaction, sender_balance: float) -> bool:
        """
        Validates a transaction before adding it to the pool.
        :param transaction: The Transaction object to validate.
        :param sender_balance: The current balance of the sender.
        :return: True if the transaction is valid, False otherwise.
        """
        if not transaction.signature:
            print("Transaction is unsigned.")
            return False
        if transaction.amount <= 0:
            print("Transaction amount must be positive.")
            return False
        if sender_balance < transaction.amount:
            print("Insufficient balance for transaction.")
            return False
        if not transaction.verify_signature(transaction.sender_public_key):
            print("Invalid transaction signature.")
            return False
        return True

    def get_pending_transactions(self, max_count: int = 10) -> List[Transaction]:
        """
        Retrieves a list of pending transactions for block creation.
        :param max_count: Maximum number of transactions to retrieve.
        :return: A list of Transaction objects.
        """
        with self.lock:
            return list(self.transactions.values())[:max_count]

    def remove_confirmed_transactions(self, confirmed_tx_hashes: List[str]):
        """
        Removes transactions from the pool that have been included in a block.
        :param confirmed_tx_hashes: List of transaction hashes to remove.
        """
        with self.lock:
            for tx_hash in confirmed_tx_hashes:
                if tx_hash in self.transactions:
                    del self.transactions[tx_hash]
            print(f"Removed {len(confirmed_tx_hashes)} confirmed transactions from the pool.")

    def prioritize_transactions(self):
        """
        Sorts transactions in the pool by fees (highest to lowest).
        This ensures high-priority transactions are included in blocks first.
        """
        with self.lock:
            self.transactions = dict(
                sorted(self.transactions.items(), key=lambda item: item[1].fee, reverse=True)
            )

    def __len__(self) -> int:
        """Returns the number of transactions in the pool."""
        return len(self.transactions)

    def __str__(self) -> str:
        """Returns a string representation of the transaction pool."""
        with self.lock:
            return "\n".join([str(tx.to_dict()) for tx in self.transactions.values()])


# Example usage
if __name__ == "__main__":
    from transactions.transaction import Transaction

    pool = TransactionPool()

    # Example private/public key generation for testing
    from cryptography.hazmat.primitives.asymmetric import rsa # type: ignore
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    # Create some dummy transactions
    tx1 = Transaction("Alice", "Bob", 10)
    tx1.sign_transaction(private_key)
    tx1.sender_public_key = public_key  # Attach public key for verification

    tx2 = Transaction("Charlie", "Dave", 20)
    tx2.sign_transaction(private_key)
    tx2.sender_public_key = public_key

    # Add transactions to the pool
    pool.add_transaction(tx1, sender_balance=50)
    pool.add_transaction(tx2, sender_balance=30)

    # Print pending transactions
    print("Pending Transactions:")
    print(pool)

    # Simulate block confirmation and remove confirmed transactions
    confirmed_hashes = [tx1.calculate_hash()]
    pool.remove_confirmed_transactions(confirmed_hashes)

    # Print pending transactions after confirmation
    print("Pending Transactions After Confirmation:")
    print(pool)
