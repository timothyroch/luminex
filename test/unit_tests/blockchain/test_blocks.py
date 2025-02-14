import unittest
import time
from blockchain.blocks.block import Block
from blockchain.blocks.block_validation import BlockValidator

class TestBlocks(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing blocks.
        """
        self.genesis_block = Block(
            index=0,
            previous_hash="0" * 64,
            data="Genesis Block",
            timestamp=1673367600,
            nonce=0
        )
        self.new_block = Block(
            index=1,
            previous_hash=self.genesis_block.hash,
            data="Block 1 Data",
            timestamp=int(time.time()),
            nonce=12345
        )
        self.block_validator = BlockValidator()

    def test_block_creation(self):
        """
        Test the creation of a block and its basic structure.
        """
        self.assertEqual(self.genesis_block.index, 0, "Genesis block index should be 0")
        self.assertEqual(len(self.genesis_block.hash), 64, "Block hash should be 64 characters long")
        print("Block creation test passed.")

    def test_block_hash_integrity(self):
        """
        Test that the block hash is correctly calculated and remains consistent.
        """
        original_hash = self.genesis_block.hash
        recalculated_hash = self.genesis_block.calculate_hash()
        self.assertEqual(original_hash, recalculated_hash, "Block hash integrity check failed")
        print("Block hash integrity test passed.")

    def test_block_validation(self):
        """
        Test that a valid block passes validation.
        """
        is_valid = self.block_validator.validate_block(self.new_block, self.genesis_block)
        self.assertTrue(is_valid, "Valid block failed validation")
        print("Block validation test passed.")

    def test_invalid_block_rejection(self):
        """
        Test that an invalid block is rejected during validation.
        """
        invalid_block = Block(
            index=1,
            previous_hash="INVALID_HASH",
            data="Invalid Block Data",
            timestamp=int(time.time()),
            nonce=12345
        )
        is_valid = self.block_validator.validate_block(invalid_block, self.genesis_block)
        self.assertFalse(is_valid, "Invalid block passed validation")
        print("Invalid block rejection test passed.")

    def test_block_chain_link(self):
        """
        Test that the block's previous hash matches the hash of the previous block.
        """
        self.assertEqual(self.new_block.previous_hash, self.genesis_block.hash, "Block chain link is broken")
        print("Block chain link test passed.")

if __name__ == "__main__":
    unittest.main()
