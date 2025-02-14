import unittest
from layer2_solutions.sidechains.sidechain_manager import SidechainManager
from layer2_solutions.sidechains.validator_bridge import ValidatorBridge
from layer2_solutions.sidechains.plasma.plasma_operator import PlasmaOperator
from layer2_solutions.sidechains.poa.authority_manager import AuthorityManager
from blockchain.transactions.transaction import Transaction

class TestSidechains(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing sidechains.
        """
        self.sidechain_manager = SidechainManager()
        self.validator_bridge = ValidatorBridge()
        self.plasma_operator = PlasmaOperator()
        self.authority_manager = AuthorityManager()
        
        # Sample sidechain and transactions
        self.sidechain = self.sidechain_manager.create_sidechain("PlasmaChain", "plasma")
        self.transaction = Transaction(
            sender="address1",
            recipient="address2",
            amount=100,
            timestamp=1673367600,
            signature="VALID_SIGNATURE"
        )

    def test_create_sidechain(self):
        """
        Test that a sidechain is successfully created.
        """
        self.assertEqual(self.sidechain.name, "PlasmaChain", "Sidechain creation failed")
        self.assertEqual(self.sidechain.type, "plasma", "Sidechain type mismatch")
        print("Sidechain creation test passed.")

    def test_l1_to_sidechain_communication(self):
        """
        Test communication between Layer 1 and the sidechain via the validator bridge.
        """
        success = self.validator_bridge.send_transaction_to_sidechain(self.sidechain, self.transaction)
        self.assertTrue(success, "Failed to send transaction from Layer 1 to sidechain")
        print("L1 to sidechain communication test passed.")

    def test_plasma_transaction_aggregation(self):
        """
        Test that the Plasma operator correctly aggregates transactions.
        """
        self.plasma_operator.add_transaction(self.transaction)
        aggregated_transactions = self.plasma_operator.aggregate_transactions()
        self.assertIn(self.transaction, aggregated_transactions, "Transaction aggregation in Plasma operator failed")
        print("Plasma transaction aggregation test passed.")

    def test_poa_authority_assignment(self):
        """
        Test that authorities are correctly assigned in a PoA sidechain.
        """
        self.authority_manager.add_authority("validator1")
        self.authority_manager.add_authority("validator2")
        authorities = self.authority_manager.get_authorities()
        self.assertIn("validator1", authorities, "Authority assignment failed for validator1")
        self.assertIn("validator2", authorities, "Authority assignment failed for validator2")
        print("PoA authority assignment test passed.")

    def test_remove_authority(self):
        """
        Test that an authority can be removed from a PoA sidechain.
        """
        self.authority_manager.add_authority("validator3")
        self.authority_manager.remove_authority("validator3")
        authorities = self.authority_manager.get_authorities()
        self.assertNotIn("validator3", authorities, "Failed to remove authority from PoA sidechain")
        print("PoA remove authority test passed.")

    def test_invalid_sidechain_type(self):
        """
        Test that creating a sidechain with an invalid type raises an error.
        """
        with self.assertRaises(ValueError):
            self.sidechain_manager.create_sidechain("InvalidChain", "invalid_type")
        print("Invalid sidechain type test passed.")

if __name__ == "__main__":
    unittest.main()
