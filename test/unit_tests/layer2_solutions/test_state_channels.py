import unittest
from layer2_solutions.state_channels.state_channel_manager import StateChannelManager
from layer2_solutions.state_channels.offchain_signing import OffchainSigner
from layer2_solutions.state_channels.channel_settlement import ChannelSettlement
from blockchain.transactions.transaction import Transaction

class TestStateChannels(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing state channels.
        """
        self.state_channel_manager = StateChannelManager()
        self.offchain_signer = OffchainSigner()
        self.channel_settlement = ChannelSettlement()

        # Sample state channel and transactions
        self.channel_id = self.state_channel_manager.open_channel(
            sender="address1", recipient="address2", initial_balance=100
        )
        self.transaction = Transaction(
            sender="address1",
            recipient="address2",
            amount=20,
            timestamp=1673367600,
            signature=""
        )

    def test_open_channel(self):
        """
        Test that a state channel is successfully opened.
        """
        channel = self.state_channel_manager.get_channel(self.channel_id)
        self.assertEqual(channel["sender"], "address1", "Sender mismatch in state channel")
        self.assertEqual(channel["recipient"], "address2", "Recipient mismatch in state channel")
        self.assertEqual(channel["balance"], 100, "Initial balance mismatch in state channel")
        print("Open channel test passed.")

    def test_offchain_transaction_signing(self):
        """
        Test that an off-chain transaction is correctly signed and verified.
        """
        signature = self.offchain_signer.sign_transaction(self.transaction, private_key="PRIVATE_KEY1")
        self.transaction.signature = signature
        is_verified = self.offchain_signer.verify_transaction(self.transaction, public_key="PUBLIC_KEY1")
        self.assertTrue(is_verified, "Off-chain transaction signature verification failed")
        print("Off-chain transaction signing test passed.")

    def test_update_channel_balance(self):
        """
        Test that the state channel balance is updated correctly after an off-chain transaction.
        """
        self.state_channel_manager.update_channel_balance(self.channel_id, amount=20)
        channel = self.state_channel_manager.get_channel(self.channel_id)
        self.assertEqual(channel["balance"], 80, "Channel balance not updated correctly")
        print("Update channel balance test passed.")

    def test_close_channel(self):
        """
        Test that a state channel can be successfully closed.
        """
        final_balance = self.state_channel_manager.close_channel(self.channel_id)
        self.assertEqual(final_balance, 80, "Final balance after closing channel is incorrect")
        print("Close channel test passed.")

    def test_settle_channel_on_chain(self):
        """
        Test that the final state of a channel is correctly settled on-chain.
        """
        on_chain_balance = self.channel_settlement.settle_on_chain(self.channel_id, final_balance=80)
        self.assertEqual(on_chain_balance, 80, "On-chain settlement balance mismatch")
        print("Settle channel on-chain test passed.")

    def test_invalid_channel_operations(self):
        """
        Test that invalid operations on a non-existent channel are rejected.
        """
        with self.assertRaises(ValueError):
            self.state_channel_manager.get_channel("invalid_channel_id")
        print("Invalid channel operation test passed.")

if __name__ == "__main__":
    unittest.main()
