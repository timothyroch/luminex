import unittest
from blockchain.state.state_manager import StateManager
from blockchain.state.utxo_set import UTXOSet
from blockchain.state.smart_contracts import SmartContract
from blockchain.blocks.block import Block
from blockchain.transactions.transaction import Transaction

class TestState(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing state management.
        """
        self.state_manager = StateManager()
        self.utxo_set = UTXOSet()
        self.smart_contract = SmartContract(contract_address="contract1", initial_state={"balance": 1000})

        # Genesis block to initialize the state
        self.genesis_block = Block(
            index=0,
            previous_hash="0" * 64,
            data="Genesis Block",
            timestamp=1673367600,
            nonce=0
        )

        # Sample transaction to test UTXO updates
        self.transaction = Transaction(
            sender="address1",
            recipient="address2",
            amount=100,
            timestamp=1673368600,
            signature="VALID_SIGNATURE"
        )

    def test_initialize_state(self):
        """
        Test that the state is correctly initialized with the genesis block.
        """
        self.state_manager.initialize_state(self.genesis_block)
        self.assertIn(self.genesis_block.hash, self.state_manager.state, "Genesis block not found in state")
        print("State initialization test passed.")

    def test_apply_transaction(self):
        """
        Test that a valid transaction updates the state correctly.
        """
        self.state_manager.apply_transaction(self.transaction)
        balance = self.state_manager.get_balance("address2")
        self.assertEqual(balance, 100, "Recipient balance not updated correctly")
        print("Transaction application test passed.")

    def test_invalid_transaction(self):
        """
        Test that an invalid transaction does not update the state.
        """
        invalid_transaction = Transaction(
            sender="address1",
            recipient="address2",
            amount=100000,  # Exceeds available balance
            timestamp=1673368600,
            signature="INVALID_SIGNATURE"
        )
        with self.assertRaises(ValueError):
            self.state_manager.apply_transaction(invalid_transaction)
        print("Invalid transaction rejection test passed.")

    def test_utxo_update(self):
        """
        Test that the UTXO set is correctly updated after a transaction.
        """
        self.utxo_set.update_utxo(self.transaction)
        utxos = self.utxo_set.get_utxos("address2")
        self.assertEqual(len(utxos), 1, "UTXO not updated correctly")
        print("UTXO update test passed.")

    def test_smart_contract_execution(self):
        """
        Test that a smart contract executes correctly and updates its state.
        """
        self.smart_contract.execute({"type": "transfer", "amount": 200})
        self.assertEqual(self.smart_contract.state["balance"], 800, "Smart contract state not updated correctly")
        print("Smart contract execution test passed.")

    def test_state_persistence(self):
        """
        Test that the global state persists after updates.
        """
        self.state_manager.apply_transaction(self.transaction)
        self.state_manager.save_state("state_snapshot.json")
        loaded_state = self.state_manager.load_state("state_snapshot.json")
        self.assertIn(self.transaction.hash, loaded_state, "State persistence failed")
        print("State persistence test passed.")

if __name__ == "__main__":
    unittest.main()
