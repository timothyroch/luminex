import random
import string
import time
from hashlib import sha256
from blockchain.transactions.transaction import Transaction
from blockchain.blocks.block import Block
from cryptocurrency.wallet.wallet_utils import WalletUtils

class MockDataGenerator:
    def __init__(self):
        self.wallet_utils = WalletUtils()

    def generate_random_address(self):
        """
        Generate a random blockchain address.
        """
        return "0x" + "".join(random.choices(string.hexdigits, k=40)).lower()

    def generate_random_transaction(self, sender=None, recipient=None, max_amount=100):
        """
        Generate a mock transaction with random data.
        """
        sender = sender or self.generate_random_address()
        recipient = recipient or self.generate_random_address()
        amount = random.randint(1, max_amount)
        timestamp = int(time.time())
        transaction = Transaction(
            sender=sender,
            recipient=recipient,
            amount=amount,
            timestamp=timestamp,
            signature="MOCK_SIGNATURE"
        )
        return transaction

    def generate_mock_block(self, previous_hash, num_transactions=5):
        """
        Generate a mock block with a given number of random transactions.
        """
        transactions = [
            self.generate_random_transaction() for _ in range(num_transactions)
        ]
        timestamp = int(time.time())
        block_data = "".join(tx.to_dict()["sender"] for tx in transactions)
        block_hash = sha256(block_data.encode()).hexdigest()
        return Block(
            index=random.randint(1, 1000),
            previous_hash=previous_hash,
            data=transactions,
            timestamp=timestamp,
            nonce=random.randint(0, 100000),
            hash=block_hash
        )

    def generate_mock_wallet(self):
        """
        Generate a mock wallet with a key pair and an address.
        """
        private_key, public_key = self.wallet_utils.generate_key_pair()
        address = self.wallet_utils.get_address(public_key)
        return {
            "private_key": private_key,
            "public_key": public_key,
            "address": address
        }

    def generate_mock_data(self, num_wallets=5, num_blocks=3):
        """
        Generate a complete set of mock data, including wallets and blocks.
        """
        wallets = [self.generate_mock_wallet() for _ in range(num_wallets)]
        blocks = []
        previous_hash = "0" * 64  # Genesis block hash
        for _ in range(num_blocks):
            block = self.generate_mock_block(previous_hash)
            blocks.append(block)
            previous_hash = block.hash
        return {"wallets": wallets, "blocks": blocks}

# Usage example
if __name__ == "__main__":
    generator = MockDataGenerator()
    mock_data = generator.generate_mock_data(num_wallets=3, num_blocks=2)
    
    print("Generated Mock Wallets:")
    for wallet in mock_data["wallets"]:
        print(wallet)
    
    print("\nGenerated Mock Blocks:")
    for block in mock_data["blocks"]:
        print(block.to_dict())
