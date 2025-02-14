import json
import logging
from blockchain.transactions.transaction_pool import TransactionPool
from blocks.blockchain_state import Blockchain
from consensus.consensus_engine import ConsensusEngine

# Initialize components
transaction_pool = TransactionPool()
blockchain = Blockchain()
consensus_engine = ConsensusEngine()

# Configure logging
logging.basicConfig(filename="monitoring/logs/message_handler.log", level=logging.INFO, format="%(asctime)s - %(message)s")

class MessageHandler:
    """Handles incoming and outgoing messages in the P2P network."""

    def __init__(self):
        self.message_types = {
            "transaction": self.handle_transaction,
            "block": self.handle_block,
            "consensus": self.handle_consensus_message,
            "node_info": self.handle_node_info
        }

    def parse_message(self, raw_message):
        """
        Parses a raw message and routes it to the appropriate handler.
        :param raw_message: The raw JSON message as a string.
        :return: Response message or None.
        """
        try:
            message = json.loads(raw_message)
            message_type = message.get("type")
            if message_type in self.message_types:
                return self.message_types[message_type](message)
            else:
                logging.warning(f"Unknown message type: {message_type}")
                return {"status": "error", "message": "Unknown message type"}
        except json.JSONDecodeError:
            logging.error("Failed to decode message: Invalid JSON format")
            return {"status": "error", "message": "Invalid JSON format"}

    def handle_transaction(self, message):
        """
        Handles a transaction message.
        :param message: The transaction message.
        :return: Response indicating success or failure.
        """
        transaction = message.get("data")
        if not transaction:
            logging.warning("Received invalid transaction message with no data")
            return {"status": "error", "message": "No transaction data provided"}

        success = transaction_pool.add_transaction(transaction, sender_balance=blockchain.get_balance(transaction["sender"]))
        if success:
            logging.info(f"Transaction added to pool: {transaction}")
            return {"status": "success", "message": "Transaction accepted"}
        else:
            logging.warning(f"Failed to add transaction: {transaction}")
            return {"status": "error", "message": "Transaction rejected"}

    def handle_block(self, message):
        """
        Handles a block message.
        :param message: The block message.
        :return: Response indicating success or failure.
        """
        block = message.get("data")
        if not block:
            logging.warning("Received invalid block message with no data")
            return {"status": "error", "message": "No block data provided"}

        success = blockchain.add_block(block, difficulty=block.get("difficulty", 2))
        if success:
            logging.info(f"Block added to blockchain: {block['hash']}")
            return {"status": "success", "message": "Block accepted"}
        else:
            logging.warning(f"Failed to add block: {block['hash']}")
            return {"status": "error", "message": "Block rejected"}

    def handle_consensus_message(self, message):
        """
        Handles a consensus-related message.
        :param message: The consensus message.
        :return: Response indicating success or failure.
        """
        consensus_data = message.get("data")
        if not consensus_data:
            logging.warning("Received invalid consensus message with no data")
            return {"status": "error", "message": "No consensus data provided"}

        result = consensus_engine.process_message(consensus_data)
        logging.info(f"Consensus message processed: {consensus_data}")
        return {"status": "success", "message": "Consensus message processed", "result": result}

    def handle_node_info(self, message):
        """
        Handles a node information message (e.g., for peer discovery).
        :param message: The node information message.
        :return: Response indicating success or failure.
        """
        node_info = message.get("data")
        if not node_info:
            logging.warning("Received invalid node info message with no data")
            return {"status": "error", "message": "No node info provided"}

        # Process node information (e.g., add to peer list)
        logging.info(f"Node info received: {node_info}")
        return {"status": "success", "message": "Node info received"}

# Example usage
if __name__ == "__main__":
    handler = MessageHandler()

    # Simulate handling a transaction message
    transaction_message = json.dumps({
        "type": "transaction",
        "data": {"sender": "Alice", "receiver": "Bob", "amount": 50}
    })
    print(handler.parse_message(transaction_message))

    # Simulate handling a block message
    block_message = json.dumps({
        "type": "block",
        "data": {"index": 5, "hash": "abc123", "previous_hash": "def456", "transactions": [], "difficulty": 2}
    })
    print(handler.parse_message(block_message))
