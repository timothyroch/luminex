import time
from typing import List, Dict, Any


class BatchProcessor:
    """Handles batching of transactions for Layer 2 solutions."""

    def __init__(self, batch_size: int = 100, timeout_seconds: int = 60):
        """
        Initializes the BatchProcessor.
        :param batch_size: Maximum number of transactions per batch.
        :param timeout_seconds: Maximum time to wait before submitting a batch.
        """
        self.batch_size = batch_size
        self.timeout_seconds = timeout_seconds
        self.pending_transactions = []
        self.batches = []
        self.last_batch_time = time.time()

    def add_transaction(self, transaction: Dict[str, Any]) -> bool:
        """
        Adds a transaction to the pending transaction pool.
        :param transaction: The transaction data.
        :return: True if the transaction was added successfully, False otherwise.
        """
        if not transaction or "id" not in transaction:
            print("Invalid transaction data.")
            return False

        self.pending_transactions.append(transaction)
        print(f"Transaction {transaction['id']} added to the pool.")
        return True

    def process_batch(self) -> bool:
        """
        Processes a batch of transactions, either when the batch size is met or the timeout is reached.
        :return: True if a batch was processed, False otherwise.
        """
        if len(self.pending_transactions) < self.batch_size and time.time() - self.last_batch_time < self.timeout_seconds:
            print("Batch conditions not met (size or timeout).")
            return False

        batch = self.pending_transactions[:self.batch_size]
        self.pending_transactions = self.pending_transactions[self.batch_size:]
        batch_id = len(self.batches) + 1

        processed_batch = {
            "batch_id": batch_id,
            "transactions": batch,
            "timestamp": time.time(),
        }
        self.batches.append(processed_batch)
        self.last_batch_time = time.time()

        print(f"Batch {batch_id} processed with {len(batch)} transactions.")
        return True

    def list_batches(self) -> List[Dict[str, Any]]:
        """
        Lists all processed batches.
        :return: A list of processed batches.
        """
        return self.batches

    def get_pending_transactions(self) -> List[Dict[str, Any]]:
        """
        Retrieves all pending transactions that haven't been batched yet.
        :return: A list of pending transactions.
        """
        return self.pending_transactions

    def flush_pending_transactions(self) -> None:
        """
        Flushes all pending transactions into a final batch.
        """
        while self.pending_transactions:
            self.process_batch()
        print("All pending transactions have been flushed into batches.")


# Example usage
if __name__ == "__main__":
    processor = BatchProcessor(batch_size=3, timeout_seconds=10)

    # Add transactions
    processor.add_transaction({"id": "tx1", "sender": "address1", "receiver": "address2", "amount": 50.0})
    processor.add_transaction({"id": "tx2", "sender": "address3", "receiver": "address4", "amount": 75.0})
    processor.add_transaction({"id": "tx3", "sender": "address5", "receiver": "address6", "amount": 20.0})
    processor.add_transaction({"id": "tx4", "sender": "address7", "receiver": "address8", "amount": 100.0})

    # Process a batch (will process if batch size or timeout is met)
    processor.process_batch()

    # List all batches
    print("\nProcessed Batches:")
    for batch in processor.list_batches():
        print(batch)

    # Show pending transactions
    print("\nPending Transactions:")
    print(processor.get_pending_transactions())

    # Flush all pending transactions
    processor.flush_pending_transactions()

    # List all batches after flush
    print("\nBatches After Flush:")
    for batch in processor.list_batches():
        print(batch)
