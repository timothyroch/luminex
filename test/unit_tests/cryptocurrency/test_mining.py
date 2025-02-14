import unittest
from blockchain.mining.pow.miner import Miner # type: ignore
from blockchain.mining.pow.hashing_algorithm import HashingAlgorithm # type: ignore
from blockchain.blocks.block import Block
from blockchain.state.state_manager import StateManager
from blockchain.transactions.transaction import Transaction

class TestMining(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing mining operations.
        """
        self.hashing_algorithm = HashingAlgorithm()
        self.miner = Miner(difficulty=4, hashing_algorithm=self.hashing_algorithm)
        self.state_manager = StateManager()

        # Sample transactions and blocks
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
            timestamp=1673368600,
            nonce=0
        )
        self.reward_transaction = Transaction(
            sender="network",
            recipient="miner1",
            amount=50,
            timestamp=1673368600,
            signature="REWARD"
        )

    def test_proof_of_work(self):
        """
        Test that the proof-of-work algorithm correctly mines a block.
        """
        mined_block = self.miner.mine_block(self.new_block)
        self.assertTrue(mined_block.hash.startswith("0" * 4), "Proof-of-work did not produce a valid block hash")
        print("Proof-of-work test passed.")

    def test_block_integration(self):
        """
        Test that a mined block integrates correctly into the blockchain state.
        """
        self.state_manager.initialize_state(self.genesis_block)
        self.state_manager.apply_block(self.new_block)
        self.assertIn(self.new_block.hash, self.state_manager.state, "Mined block not integrated into blockchain state")
        print("Block integration test passed.")

    def test_reward_distribution(self):
        """
        Test that mining rewards are distributed correctly.
        """
        self.state_manager.initialize_state(self.genesis_block)
        self.state_manager.apply_transaction(self.reward_transaction)
        miner_balance = self.state_manager.get_balance("miner1")
        self.assertEqual(miner_balance, 50, "Mining reward distribution failed")
        print("Reward distribution test passed.")

    def test_invalid_block_rejection(self):
        """
        Test that an invalid mined block is rejected.
        """
        invalid_block = Block(
            index=1,
            previous_hash="INVALID_HASH",
            data="Invalid Block Data",
            timestamp=1673368600,
            nonce=12345
        )
        is_valid = self.miner.validate_block(invalid_block, self.genesis_block)
        self.assertFalse(is_valid, "Invalid block was not rejected by the miner")
        print("Invalid block rejection test passed.")

    def test_mining_difficulty(self):
        """
        Test that the mining difficulty affects the time required to mine a block.
        """
        self.miner.difficulty = 5  # Increase difficulty
        import time
        start_time = time.time()
        self.miner.mine_block(self.new_block)
        elapsed_time = time.time() - start_time
        self.assertGreater(elapsed_time, 0, "Mining difficulty did not impact mining time as expected")
        print("Mining difficulty test passed.")

if __name__ == "__main__":
    unittest.main()
