import time
import hashlib
from typing import List, Dict
from random import choices


class HybridMining:
    """Implements a hybrid Proof of Work (PoW) and Proof of Stake (PoS) consensus mechanism."""

    def __init__(self, pow_difficulty: int, pos_weight: float, block_reward: float):
        """
        Initializes the hybrid mining system.
        :param pow_difficulty: Difficulty level for PoW mining.
        :param pos_weight: Weightage of PoS in block validation (0.0 to 1.0).
        :param block_reward: Reward for successfully mining a block.
        """
        self.pow_difficulty = pow_difficulty
        self.pos_weight = pos_weight
        self.block_reward = block_reward
        self.stakes = {}  # Stores stakes {address: amount}
        self.chain = []   # Stores mined blocks

    def proof_of_work(self, block_data: str) -> (str, int):
        """
        Performs the Proof of Work mining process.
        :param block_data: The data to include in the block.
        :return: A tuple of the valid hash and nonce.
        """
        nonce = 0
        while True:
            hash_value = hashlib.sha256(f"{block_data}{nonce}".encode('utf-8')).hexdigest()
            if hash_value.startswith('0' * self.pow_difficulty):
                return hash_value, nonce
            nonce += 1

    def proof_of_stake(self) -> str:
        """
        Selects a validator based on their stake using weighted random selection.
        :return: Selected validator's address.
        """
        if not self.stakes:
            raise ValueError("No validators available for PoS.")
        addresses, weights = zip(*self.stakes.items())
        return choices(addresses, weights=weights)[0]

    def mine_block(self, miner_address: str, block_data: str) -> Dict:
        """
        Mines a new block using the hybrid PoW-PoS consensus mechanism.
        :param miner_address: The address of the PoW miner.
        :param block_data: The data to include in the block.
        :return: The mined block as a dictionary.
        """
        # Perform Proof of Work
        pow_hash, nonce = self.proof_of_work(block_data)
        print(f"PoW completed by {miner_address} with nonce {nonce} and hash {pow_hash}")

        # Perform Proof of Stake
        pos_validator = self.proof_of_stake()
        print(f"PoS validator selected: {pos_validator}")

        # Create the block
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time.time(),
            "miner": miner_address,
            "validator": pos_validator,
            "data": block_data,
            "pow_hash": pow_hash,
            "nonce": nonce,
            "reward": self.block_reward,
            "previous_hash": self.chain[-1]["pow_hash"] if self.chain else "0"
        }

        # Append block to the chain
        self.chain.append(block)

        # Reward miner and validator
        self.stakes[pos_validator] += self.block_reward * self.pos_weight
        return block

    def add_stake(self, address: str, amount: float):
        """
        Adds stake for a given address.
        :param address: The address to stake.
        :param amount: The amount to stake.
        """
        if amount <= 0:
            raise ValueError("Stake amount must be positive.")
        self.stakes[address] = self.stakes.get(address, 0.0) + amount

    def get_chain(self) -> List[Dict]:
        """
        Returns the current blockchain.
        :return: A list of blocks.
        """
        return self.chain

    def get_stakes(self) -> Dict[str, float]:
        """
        Returns the current stakes.
        :return: A dictionary of stakes {address: amount}.
        """
        return self.stakes


# Example usage
if __name__ == "__main__":
    hybrid_miner = HybridMining(pow_difficulty=4, pos_weight=0.3, block_reward=10)

    # Add stakes
    hybrid_miner.add_stake("validator1", 100)
    hybrid_miner.add_stake("validator2", 200)
    hybrid_miner.add_stake("validator3", 300)

    # Mine a block
    block = hybrid_miner.mine_block(miner_address="miner1", block_data="Transaction data")
    print("\nMined Block:", block)

    # Print the blockchain
    print("\nBlockchain:", hybrid_miner.get_chain())

    # Print current stakes
    print("\nStakes:", hybrid_miner.get_stakes())
