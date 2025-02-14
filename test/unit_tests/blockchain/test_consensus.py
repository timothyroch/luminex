import unittest
from blockchain.consensus.consensus_engine import ConsensusEngine
from blockchain.consensus.validator_selection import ValidatorSelection
from blockchain.blocks.block import Block

class TestConsensus(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing consensus mechanisms.
        """
        self.consensus_engine = ConsensusEngine()
        self.validator_selection = ValidatorSelection()
        self.block = Block(index=1, previous_hash="0" * 64, data="Test Data", timestamp=1673367600, nonce=0)
        self.validators = ["validator1", "validator2", "validator3"]

    def test_validator_selection(self):
        """
        Test that the validator selection mechanism selects a valid validator.
        """
        selected_validator = self.validator_selection.select_validator(self.validators, round_number=1)
        self.assertIn(selected_validator, self.validators, "Selected validator is not in the list of validators")

    def test_block_proposal(self):
        """
        Test that a valid block proposal passes consensus.
        """
        is_valid = self.consensus_engine.propose_block(self.block, proposer="validator1")
        self.assertTrue(is_valid, "Block proposal failed when it should have passed")

    def test_invalid_block_rejection(self):
        """
        Test that an invalid block proposal is rejected by consensus.
        """
        invalid_block = Block(index=1, previous_hash="INVALID_HASH", data="Invalid Data", timestamp=1673367600, nonce=0)
        is_valid = self.consensus_engine.propose_block(invalid_block, proposer="validator2")
        self.assertFalse(is_valid, "Invalid block proposal passed when it should have been rejected")

    def test_block_finalization(self):
        """
        Test that a block is finalized after reaching consensus.
        """
        self.consensus_engine.propose_block(self.block, proposer="validator1")
        finalized = self.consensus_engine.finalize_block(self.block)
        self.assertTrue(finalized, "Block was not finalized after reaching consensus")

    def test_slashing_for_malicious_validator(self):
        """
        Test that malicious validators are slashed appropriately.
        """
        malicious_validator = "validator3"
        self.consensus_engine.slash_validator(malicious_validator)
        self.assertNotIn(malicious_validator, self.consensus_engine.active_validators, "Malicious validator was not slashed")

    def test_consensus_round(self):
        """
        Test a full consensus round, including block proposal, validation, and finalization.
        """
        selected_validator = self.validator_selection.select_validator(self.validators, round_number=2)
        proposed_block = Block(index=2, previous_hash=self.block.hash, data="Round 2 Data", timestamp=1673368600, nonce=0)

        # Propose and validate the block
        self.consensus_engine.propose_block(proposed_block, proposer=selected_validator)
        is_finalized = self.consensus_engine.finalize_block(proposed_block)

        self.assertTrue(is_finalized, "Consensus round failed to finalize the block")

if __name__ == "__main__":
    unittest.main()
