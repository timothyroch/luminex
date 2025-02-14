import socket
import threading
import json
from blockchain.transactions.transaction import Transaction
from transactions.transaction_pool import TransactionPool
from blocks.blockchain_state import Blockchain
from blocks.block import Block


class P2PNode:
    def __init__(self, host: str, port: int, blockchain: Blockchain, transaction_pool: TransactionPool):
        self.host = host
        self.port = port
        self.peers = []  # List of connected peers
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        """Starts the P2P server."""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"P2P Node started on {self.host}:{self.port}")
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        """Accepts incoming connections from peers."""
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Connected to peer: {address}")
            self.peers.append(client_socket)
            threading.Thread(target=self.handle_peer, args=(client_socket,), daemon=True).start()

    def handle_peer(self, client_socket):
        """Handles incoming messages from a peer."""
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    self.process_message(json.loads(message))
            except (ConnectionResetError, json.JSONDecodeError):
                print("Peer disconnected.")
                self.peers.remove(client_socket)
                break

    def process_message(self, message: dict):
        """Processes incoming messages based on their type."""
        msg_type = message.get("type")
        data = message.get("data")

        if msg_type == "transaction":
            self.handle_new_transaction(data)
        elif msg_type == "block":
            self.handle_new_block(data)
        elif msg_type == "sync_request":
            self.send_blockchain()
        else:
            print("Unknown message type received.")

    def handle_new_transaction(self, transaction_data: dict):
        """Handles a new transaction received from a peer."""
        transaction = Transaction.from_dict(transaction_data)
        sender_balance = self.get_balance(transaction.sender)  # Replace with actual balance logic
        if self.transaction_pool.add_transaction(transaction, sender_balance):
            self.broadcast({"type": "transaction", "data": transaction.to_dict()})

    def handle_new_block(self, block_data: dict):
        """Handles a new block received from a peer."""
        block = Block.from_dict(block_data)
        difficulty = 2  # Replace with actual difficulty logic
        if self.blockchain.add_block(block, difficulty):
            print(f"Block #{block.index} added to the chain.")
            self.broadcast({"type": "block", "data": block.to_dict()})

    def send_blockchain(self):
        """Sends the entire blockchain to a peer who requested it."""
        chain_data = [block.to_dict() for block in self.blockchain.chain]
        self.broadcast({"type": "sync_response", "data": chain_data})

    def broadcast(self, message: dict):
        """Broadcasts a message to all connected peers."""
        for peer in self.peers:
            try:
                peer.sendall(json.dumps(message).encode('utf-8'))
            except BrokenPipeError:
                print("Failed to send message to a peer.")

    def get_balance(self, address: str) -> float:
        """Dummy method to get a balance. Replace with actual state logic."""
        return 100.0  # Example balance


# Example usage
if __name__ == "__main__":
    blockchain = Blockchain()
    transaction_pool = TransactionPool()
    node = P2PNode("localhost", 5000, blockchain, transaction_pool)
    node.start()

    # Add some peers for demonstration
    threading.Thread(target=lambda: P2PNode("localhost", 5001, blockchain, transaction_pool).start(), daemon=True).start()
