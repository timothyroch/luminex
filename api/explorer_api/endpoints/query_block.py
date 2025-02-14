from flask import Blueprint, jsonify # type: ignore
from blocks.blockchain_state import Blockchain

# Create a blueprint for block-related endpoints
query_block_bp = Blueprint('query_block', __name__)

# Assume blockchain instance is globally accessible or passed via dependency injection
blockchain = Blockchain()

@query_block_bp.route('/block/index/<int:index>', methods=['GET'])
def get_block_by_index(index):
    """Fetches a block by its index."""
    if 0 <= index < len(blockchain.chain):
        block = blockchain.chain[index].to_dict()
        return jsonify(block), 200
    else:
        return jsonify({"error": "Block not found"}), 404

@query_block_bp.route('/block/hash/<string:block_hash>', methods=['GET'])
def get_block_by_hash(block_hash):
    """Fetches a block by its hash."""
    for block in blockchain.chain:
        if block.hash == block_hash:
            return jsonify(block.to_dict()), 200
    return jsonify({"error": "Block not found"}), 404
