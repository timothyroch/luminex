import unittest
from blocks.block import Block
from flask import Flask # type: ignore
from explorer_api.endpoints.query_block import query_block_bp
from explorer_api.endpoints.query_transaction import query_transaction_bp
from explorer_api.endpoints.query_address import query_address_bp
from blocks.blockchain_state import Blockchain
from transactions.transaction_pool import TransactionPool

# Initialize Flask app for testing
app = Flask(__name__)
app.register_blueprint(query_block_bp, url_prefix="/api")
app.register_blueprint(query_transaction_bp, url_prefix="/api")
app.register_blueprint(query_address_bp, url_prefix="/api")

# Mock instances of blockchain and transaction pool
blockchain = Blockchain()
transaction_pool = TransactionPool()

class TestExplorerAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        # Add mock data to blockchain
        blockchain.create_genesis_block()
        tx1 = {"sender": "Alice", "receiver": "Bob", "amount": 10}
        tx2 = {"sender": "Charlie", "receiver": "Dave", "amount": 20}
        block = blockchain.get_latest_block()
        new_block = Block(block.index + 1, block.hash, [tx1, tx2])
        blockchain.add_block(new_block, difficulty=2)

        # Add mock transaction to the pool
        transaction_pool.add_transaction({"sender": "Eve", "receiver": "Frank", "amount": 30}, sender_balance=100)

    def test_get_block_by_index(self):
        response = self.client.get('/api/block/index/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("transactions", response.json)

    def test_get_block_by_invalid_index(self):
        response = self.client.get('/api/block/index/100')
        self.assertEqual(response.status_code, 404)

    def test_get_transaction_by_hash(self):
        tx_hash = blockchain.chain[1].transactions[0].get("hash")
        response = self.client.get(f'/api/transaction/{tx_hash}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("transaction", response.json)

    def test_get_transaction_invalid_hash(self):
        response = self.client.get('/api/transaction/invalidhash123')
        self.assertEqual(response.status_code, 404)

    def test_get_address_details(self):
        response = self.client.get('/api/address/Bob')
        self.assertEqual(response.status_code, 200)
        self.assertIn("balance", response.json)
        self.assertIn("transactions", response.json)

    def test_get_address_no_transactions(self):
        response = self.client.get('/api/address/Unknown')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["balance"], 0)
        self.assertEqual(len(response.json["transactions"]), 0)

if __name__ == '__main__':
    unittest.main()
