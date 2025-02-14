from typing import Dict, Any, List, Optional


class ExplorerService:
    """Core service for querying blockchain data."""

    def __init__(self, blockchain_node: Any):
        """
        Initializes the ExplorerService.
        :param blockchain_node: An instance of the blockchain node or client.
        """
        self.blockchain_node = blockchain_node

    def get_block_by_hash(self, block_hash: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves block details by its hash.
        :param block_hash: The hash of the block.
        :return: Block details or None if not found.
        """
        try:
            block = self.blockchain_node.get_block(block_hash)
            if block:
                print(f"Block {block_hash} retrieved successfully.")
                return block
            else:
                print(f"Block {block_hash} not found.")
                return None
        except Exception as e:
            print(f"Error retrieving block {block_hash}: {e}")
            return None

    def get_block_by_number(self, block_number: int) -> Optional[Dict[str, Any]]:
        """
        Retrieves block details by its number.
        :param block_number: The number of the block.
        :return: Block details or None if not found.
        """
        try:
            block = self.blockchain_node.get_block_by_number(block_number)
            if block:
                print(f"Block #{block_number} retrieved successfully.")
                return block
            else:
                print(f"Block #{block_number} not found.")
                return None
        except Exception as e:
            print(f"Error retrieving block #{block_number}: {e}")
            return None

    def get_transaction(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves transaction details by its hash.
        :param tx_hash: The hash of the transaction.
        :return: Transaction details or None if not found.
        """
        try:
            transaction = self.blockchain_node.get_transaction(tx_hash)
            if transaction:
                print(f"Transaction {tx_hash} retrieved successfully.")
                return transaction
            else:
                print(f"Transaction {tx_hash} not found.")
                return None
        except Exception as e:
            print(f"Error retrieving transaction {tx_hash}: {e}")
            return None

    def get_account_balance(self, address: str) -> Optional[float]:
        """
        Retrieves the balance of an account by its address.
        :param address: The blockchain address.
        :return: Account balance or None if not found.
        """
        try:
            balance = self.blockchain_node.get_balance(address)
            print(f"Balance for {address}: {balance}")
            return balance
        except Exception as e:
            print(f"Error retrieving balance for {address}: {e}")
            return None

    def get_transaction_history(self, address: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieves the transaction history of an account.
        :param address: The blockchain address.
        :param limit: The maximum number of transactions to retrieve.
        :return: List of transaction details.
        """
        try:
            history = self.blockchain_node.get_transaction_history(address, limit)
            print(f"Transaction history for {address} retrieved successfully.")
            return history
        except Exception as e:
            print(f"Error retrieving transaction history for {address}: {e}")
            return []


# Example usage (with a mock blockchain node)
class MockBlockchainNode:
    """Mock implementation of a blockchain node for testing purposes."""

    def get_block(self, block_hash: str) -> Dict[str, Any]:
        return {"hash": block_hash, "number": 1, "transactions": [], "timestamp": 1673445600}

    def get_block_by_number(self, block_number: int) -> Dict[str, Any]:
        return {"hash": "mockhash123", "number": block_number, "transactions": [], "timestamp": 1673445700}

    def get_transaction(self, tx_hash: str) -> Dict[str, Any]:
        return {"hash": tx_hash, "from": "address1", "to": "address2", "amount": 50.0, "timestamp": 1673445800}

    def get_balance(self, address: str) -> float:
        return 100.0

    def get_transaction_history(self, address: str, limit: int) -> List[Dict[str, Any]]:
        return [{"hash": f"tx{n}", "from": "address1", "to": "address2", "amount": n * 10.0, "timestamp": 1673445900 + n}
                for n in range(1, limit + 1)]


if __name__ == "__main__":
    node = MockBlockchainNode()
    service = ExplorerService(blockchain_node=node)

    # Retrieve block by hash
    print(service.get_block_by_hash("mockhash123"))

    # Retrieve block by number
    print(service.get_block_by_number(1))

    # Retrieve transaction
    print(service.get_transaction("tx12345"))

    # Retrieve account balance
    print(service.get_account_balance("address1"))

    # Retrieve transaction history
    print(service.get_transaction_history("address1", limit=5))
