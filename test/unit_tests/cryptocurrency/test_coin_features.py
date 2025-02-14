import unittest
from cryptocurrency.coin_features.governance.voting_mechanism import VotingMechanism
from cryptocurrency.coin_features.stablecoin.peg_manager import PegManager
from cryptocurrency.coin_features.privacy.zk_transactions import ZKTransaction

class TestCoinFeatures(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing coin features.
        """
        # Governance setup
        self.voting_mechanism = VotingMechanism()
        self.voting_mechanism.proposals = {
            "proposal1": {"votes_for": 0, "votes_against": 0},
            "proposal2": {"votes_for": 0, "votes_against": 0},
        }

        # Stablecoin setup
        self.peg_manager = PegManager(peg_ratio=1.0, reserve_balance=100000)

        # Privacy setup
        self.zk_transaction = ZKTransaction(
            sender="address1",
            recipient="address2",
            amount=100,
            proof="VALID_ZK_PROOF"
        )

    def test_governance_voting(self):
        """
        Test that governance voting correctly updates vote counts.
        """
        self.voting_mechanism.vote("proposal1", "for")
        self.assertEqual(self.voting_mechanism.proposals["proposal1"]["votes_for"], 1, "Voting for proposal failed")
        print("Governance voting test passed.")

    def test_governance_invalid_vote(self):
        """
        Test that invalid votes are rejected.
        """
        with self.assertRaises(ValueError):
            self.voting_mechanism.vote("invalid_proposal", "for")
        print("Governance invalid vote test passed.")

    def test_stablecoin_peg_maintenance(self):
        """
        Test that the stablecoin peg is maintained within acceptable limits.
        """
        self.peg_manager.adjust_peg_ratio(market_price=1.01)
        self.assertAlmostEqual(self.peg_manager.peg_ratio, 1.0, delta=0.01, msg="Stablecoin peg ratio not maintained")
        print("Stablecoin peg maintenance test passed.")

    def test_stablecoin_reserve_audit(self):
        """
        Test that the stablecoin reserve audit accurately reports reserves.
        """
        reserve = self.peg_manager.audit_reserves()
        self.assertEqual(reserve, 100000, "Stablecoin reserve audit failed")
        print("Stablecoin reserve audit test passed.")

    def test_valid_zk_transaction(self):
        """
        Test that a valid ZK transaction is accepted.
        """
        is_valid = self.zk_transaction.verify_proof()
        self.assertTrue(is_valid, "Valid ZK transaction proof failed")
        print("Valid ZK transaction test passed.")

    def test_invalid_zk_transaction(self):
        """
        Test that an invalid ZK transaction is rejected.
        """
        invalid_zk_transaction = ZKTransaction(
            sender="address1",
            recipient="address2",
            amount=100,
            proof="INVALID_ZK_PROOF"
        )
        is_valid = invalid_zk_transaction.verify_proof()
        self.assertFalse(is_valid, "Invalid ZK transaction proof passed")
        print("Invalid ZK transaction test passed.")

if __name__ == "__main__":
    unittest.main()
