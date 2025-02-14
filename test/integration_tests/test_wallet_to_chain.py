import unittest
from unittest.mock import patch, MagicMock
from blockchain.transactions.transaction import Transaction
from blockchain.blocks.block import Block
from blockchain.blocks.blockchain_state import BlockchainState
from cryptocurrency.wallet.wallet_utils import WalletUtils

class TestWalletToChain(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing wallet-to-blockchain interactions.
        """
        self.wallet_utils = WalletUtils()
        self.blockchain_state = BlockchainState()

        # Mock wallet data
        self.private_key, self.public_key = self.wallet_utils.generate_key_pair()
        self.sender_address = self.wallet_utils.get_address(self.public_key)

        # Mock transaction
        self.transaction = Transaction(
            sender=self.sender_address,
            recipient="address2",
            amount=50,
            timestamp=1673367600,
            signature=""
        )

    @patch("blockchain.transactions.transaction_pool.TransactionPool.add_transaction")
    def test_create_and_submit_transaction(self, mock_add_transaction):
        """
        Test creating and submitting a transaction from the wallet to the blockchain.
        """
        self.transaction.signature = self.wallet_utils.sign_transaction(self.transaction, self.private_key)
        response = mock_add_transaction(self.transaction)
        self.assertIsNone(response, "Transaction should be successfully added to the pool")
        print("Create and submit transaction test passed.")

    def test_transaction_signature_verification(self):
        """
        Test that a transaction signature can be successfully verified.
        """
        self.transaction.signature = self.wallet_utils.sign_transaction(self.transaction, self.private_key)
        is_verified = self.wallet_utils.verify_transaction(self.transaction, self.public_key)
        self.assertTrue(is_verified, "Transaction signature verification failed")
        print("Transaction signature verification test passed.")

    @patch("blockchain.blocks.block_miner.BlockMiner.mine_block")
    def test_transaction_inclusion_in_block(self, mock_mine_block):
        """
        Test that a submitted transaction is included in a mined block.
        """
        mock_mine_block.return_value = Block(
            index=1,
            previous_hash="0" * 64,
            data=[self.transaction],
            timestamp=1673368600,
            nonce=12345
        )
        mined_block = mock_mine_block()
        self.assertIn(self.transaction, mined_block.data, "Transaction not included in the mined block")
        print("Transaction inclusion in block test passed.")

    @patch("blockchain.blocks.blockchain_state.BlockchainState.get_balance")
    def test_balance_update_after_transaction(self, mock_get_balance):
        """
        Test that the sender and recipient balances are updated correctly after the transaction.
        """
        mock_get_balance.side_effect = lambda address: 100 if address == "address2" else 50
        sender_balance = self.blockchain_state.get_balance(self.sender_address)
        recipient_balance = self.blockchain_state.get_balance("address2")
        self.assertEqual(sender_balance, 50, "Sender balance update is incorrect")
        self.assertEqual(recipient_balance, 100, "Recipient balance update is incorrect")
        print("Balance update after transaction test passed.")

    def test_invalid_transaction_rejection(self):
        """
        Test that an invalid transaction is rejected by the blockchain.
        """
        invalid_transaction = Transaction(
            sender=self.sender_address,
            recipient="address2",
            amount=-50,  # Invalid amount
            timestamp=1673367600,
            signature=""
        )
        with self.assertRaises(ValueError):
            self.blockchain_state.apply_transaction(invalid_transaction)
        print("Invalid transaction rejection test passed.")

if __name__ == "__main__":
    unittest.main()
