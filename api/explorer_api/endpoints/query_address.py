from flask import Blueprint, jsonify # type: ignore
from blocks.blockchain_state import Blockchain

# Create a blueprint for address-related endpoints
query_address_bp = Blueprint('query_address', __name__)

# Assume blockchain instance is globally accessible
blockchain = Blockchain()

@query_address_bp.route('/address/<string:address>', methods=['GET'])
def get_address_details(address):
    """Fetches the balance and transaction history of an address."""
    balance = blockchain.get_balance(address)
    transaction_history = []

    # Search for all transactions involving the address
    for block in blockchain.chain:
        for transaction in block.transactions:
            if transaction["sender"] == address or transaction["receiver"] == address:
                transaction_history.append(transaction)

    return jsonify({
        "address": address,
        "balance": balance,
        "transactions": transaction_history
    }), 200
