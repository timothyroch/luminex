import time
from typing import Dict, List


class StakingManager:
    """Manages staking operations in a Proof of Stake system."""

    def __init__(self, min_stake: float, lock_period: int):
        """
        Initializes the StakingManager with minimum stake and lock period.
        :param min_stake: Minimum amount required to become a validator.
        :param lock_period: Lock period (in seconds) for staked tokens.
        """
        self.min_stake = min_stake
        self.lock_period = lock_period
        self.stakes: Dict[str, Dict] = {}  # Stores staking data {address: {"amount": float, "timestamp": float}}

    def stake(self, address: str, amount: float) -> str:
        """
        Stakes a specified amount for a given address.
        :param address: Wallet address of the user staking tokens.
        :param amount: Amount of tokens to stake.
        :return: Confirmation message.
        """
        if amount < self.min_stake:
            raise ValueError(f"Stake amount must be at least {self.min_stake} tokens.")

        if address in self.stakes:
            self.stakes[address]["amount"] += amount
        else:
            self.stakes[address] = {"amount": amount, "timestamp": time.time()}

        return f"Successfully staked {amount} tokens for address {address}."

    def unstake(self, address: str) -> str:
        """
        Unstakes tokens for a given address if the lock period has passed.
        :param address: Wallet address of the user unstaking tokens.
        :return: Confirmation message.
        """
        if address not in self.stakes:
            raise ValueError(f"No stakes found for address {address}.")

        stake_data = self.stakes[address]
        time_elapsed = time.time() - stake_data["timestamp"]

        if time_elapsed < self.lock_period:
            remaining_time = self.lock_period - time_elapsed
            raise ValueError(f"Tokens are still locked. Please wait {remaining_time:.2f} seconds.")

        unstaked_amount = stake_data["amount"]
        del self.stakes[address]  # Remove stake record
        return f"Successfully unstaked {unstaked_amount} tokens for address {address}."

    def get_stake(self, address: str) -> float:
        """
        Returns the staked amount for a given address.
        :param address: Wallet address of the user.
        :return: Amount of tokens staked.
        """
        return self.stakes.get(address, {}).get("amount", 0.0)

    def get_all_validators(self) -> List[str]:
        """
        Returns a list of all addresses that qualify as validators.
        :return: List of validator addresses.
        """
        return [address for address, data in self.stakes.items() if data["amount"] >= self.min_stake]

    def get_staking_info(self) -> Dict[str, Dict]:
        """
        Returns the current staking information for all participants.
        :return: Dictionary of staking data.
        """
        return self.stakes


# Example usage
if __name__ == "__main__":
    manager = StakingManager(min_stake=50.0, lock_period=10)

    try:
        # Stake tokens
        print(manager.stake("address1", 100))
        print(manager.stake("address2", 60))
        print(manager.stake("address3", 40))  # Below min_stake, should raise an error

    except ValueError as e:
        print("Error:", e)

    # Get stake info
    print("\nStaking Info:", manager.get_staking_info())

    # Get all validators
    print("\nValidators:", manager.get_all_validators())

    # Attempt to unstake before lock period
    try:
        print(manager.unstake("address1"))
    except ValueError as e:
        print("Error:", e)

    # Wait for lock period and unstake
    time.sleep(10)
    print("\nAfter lock period:")
    print(manager.unstake("address1"))

    # Check remaining staking info
    print("\nStaking Info After Unstaking:", manager.get_staking_info())
