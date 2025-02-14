from typing import Dict, List


class RewardDistribution:
    """Handles reward calculation and distribution for validators and stakers."""

    def __init__(self, total_block_reward: float, commission_rate: float = 0.1):
        """
        Initializes the RewardDistribution system.
        :param total_block_reward: Total reward for a mined or validated block.
        :param commission_rate: Percentage (as a decimal) of rewards taken as network fees or validator commission.
        """
        self.total_block_reward = total_block_reward
        self.commission_rate = commission_rate

    def calculate_rewards(self, stakes: Dict[str, float], total_stake: float) -> Dict[str, float]:
        """
        Calculates rewards for each staker based on their stake.
        :param stakes: Dictionary of stakes {address: amount}.
        :param total_stake: Total amount of tokens staked in the network.
        :return: A dictionary of rewards {address: reward}.
        """
        if total_stake == 0:
            raise ValueError("Total stake cannot be zero.")

        # Calculate the reward pool after commission
        reward_pool = self.total_block_reward * (1 - self.commission_rate)

        # Distribute rewards proportionally to each staker's contribution
        rewards = {
            address: (stake / total_stake) * reward_pool
            for address, stake in stakes.items()
        }

        return rewards

    def distribute_rewards(self, stakes: Dict[str, float], reward_pool: Dict[str, float]) -> Dict[str, float]:
        """
        Distributes the calculated rewards to each staker.
        :param stakes: Dictionary of current stakes {address: amount}.
        :param reward_pool: Dictionary of rewards {address: reward}.
        :return: Updated stakes after distributing rewards.
        """
        updated_stakes = {
            address: stakes[address] + reward_pool.get(address, 0.0)
            for address in stakes
        }
        return updated_stakes

    def calculate_and_distribute(self, stakes: Dict[str, float]) -> Dict[str, float]:
        """
        Full process of calculating and distributing rewards.
        :param stakes: Dictionary of current stakes {address: amount}.
        :return: Updated stakes after reward distribution.
        """
        total_stake = sum(stakes.values())
        rewards = self.calculate_rewards(stakes, total_stake)
        return self.distribute_rewards(stakes, rewards)


# Example usage
if __name__ == "__main__":
    stakes = {
        "address1": 100,
        "address2": 200,
        "address3": 300
    }

    reward_manager = RewardDistribution(total_block_reward=12.5, commission_rate=0.05)

    try:
        # Calculate and distribute rewards
        updated_stakes = reward_manager.calculate_and_distribute(stakes)
        print("Updated Stakes After Reward Distribution:")
        for address, amount in updated_stakes.items():
            print(f"{address}: {amount:.2f}")
    except ValueError as e:
        print("Error:", e)
