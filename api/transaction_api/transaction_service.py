import time
from typing import Dict, Any, List
from transaction_utils import generate_transaction_id, sign_transaction, verify_signature
import requests # type: ignore


class TransactionService:
    """Handles core logic for transaction operations."""

    def __init__(self):
        self.transaction_pool: List[Dict[str, Any]] = []  # In-memory transaction pool
        self.peer_nodes = [
            "http://node1.blockchain.net",
            "http://node2.blockchain.net",
            "http://node3.blockchain.net"
        ]  # Replace with dynamic discovery in production

    def create_transaction(self, sender: str, receiver: str, amount: float, private_key: str) -> Dict[str, Any]:
        """
        Creates and signs a new transaction.
        :param sender: The sender's address.
        :param receiver: The receiver's address.
        :param amount: The amount to transfer.
        :param private_key: The sender's private key.
        :return: The signed transaction.
        """
        if amount <= 0:
            raise ValueError("Transaction amount must be greater than zero.")

        transaction = {
            "id": generate_transaction_id(sender, receiver, amount, time.time()),
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "timestamp": time.time(),
        }

        # Sign the transaction
        transaction["signature"] = sign_transaction(private_key, transaction)
        self.transaction_pool.append(transaction)
        print(f"Transaction created: {transaction['id']}")
        return transaction

    def validate_transaction(self, transaction: Dict[str, Any], public_key: str) -> bool:
        """
        Validates a transaction for correctness and authenticity.
        :param transaction: The transaction data.
        :param public_key: The sender's public key.
        :return: True if the transaction is valid, False otherwise.
        """
        required_fields = ["id", "sender", "receiver", "amount", "timestamp", "signature"]
        for field in required_fields:
            if field not in transaction:
                print(f"Missing required field: {field}")
                return False

        # Validate timestamp
        current_time = time.time()
        if transaction["timestamp"] > current_time or current_time - transaction["timestamp"] > 3600:
            print("Invalid transaction timestamp.")
            return False

        # Validate signature
        is_valid_signature = verify_signature(public_key, transaction, transaction["signature"])
        if not is_valid_signature:
            print("Invalid transaction signature.")
            return False

        print(f"Transaction {transaction['id']} is valid.")
        return True

    def broadcast_transaction(self, transaction: Dict[str, Any]) -> List[str]:
        """
        Broadcasts a transaction to all peer nodes.
        :param transaction: The transaction data.
        :return: A list of peer nodes where the transaction failed to broadcast.
        """
        failed_nodes = []
        for node in self.peer_nodes:
            try:
                response = requests.post(f"{node}/receive_transaction", json=transaction, timeout=5)
                if response.status_code != 200:
                    failed_nodes.append(node)
                    print(f"Failed to broadcast to {node}. Response: {response.status_code}")
            except requests.exceptions.RequestException as e:
                failed_nodes.append(node)
                print(f"Error broadcasting to {node}: {e}")

        if not failed_nodes:
            print(f"Transaction {transaction['id']} broadcast successfully to all nodes.")
        return failed_nodes


# Example usage
if __name__ == "__main__":
    service = TransactionService()

    # Create a new transaction
    transaction = service.create_transaction(
        sender="address1",
        receiver="address2",
        amount=50.0,
        private_key="example_private_key"
    )

    # Validate the transaction
    is_valid = service.validate_transaction(transaction, public_key="sender_public_key")
    print(f"Transaction valid? {is_valid}")

    # Broadcast the transaction
    failed_nodes = service.broadcast_transaction(transaction)
    if failed_nodes:
        print("Failed to broadcast to the following nodes:", failed_nodes)
