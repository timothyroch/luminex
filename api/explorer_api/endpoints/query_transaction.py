from flask import Blueprint, jsonify # type: ignore
from blocks.blockchain_state import Blockchain
from transactions.transaction_pool import TransactionPool

# Create a blueprint for transaction-related endpoints
query_transaction_bp = Blueprint('query_transaction', __name__)

# Assume blockchain and transaction_pool instances are globally accessible
blockchain = Blockchain()
transaction_pool = TransactionPool()

@query_transaction_bp.route('/transaction/<string:tx_hash>', methods=['GET'])
def get_transaction_by_hash(tx_hash):
    """Fetches a transaction by its hash."""
    # Search in blockchain
    for block in blockchain.chain:
        for transaction in block.transactions:
            if transaction.get("hash") == tx_hash:
                return jsonify({
                    "status": "confirmed",
                    "transaction": transaction,
                    "block_index": block.index
                }), 200

    # Search in transaction pool
    for tx in transaction_pool.transactions.values():
        if tx.calculate_hash() == tx_hash:
            return jsonify({
                "status": "pending",
                "transaction": tx.to_dict()
            }), 200

    # Transaction not found
    return jsonify({"error": "Transaction not found"}), 404
