from typing import Dict


class RewardToken:
    """Handles the logic for issuing and managing reward tokens."""

    def __init__(self, token_name: str, total_supply: int, reward_rate: float):
        """
        Initializes the RewardToken system.
        :param token_name: Name of the reward token.
        :param total_supply: Maximum total supply of the reward token.
        :param reward_rate: Reward rate per eligible activity (e.g., per transaction, per stake).
        """
        self.token_name = token_name
        self.total_supply = total_supply
        self.reward_rate = reward_rate
        self.current_supply = 0
        self.balances = {}  # User balances {address: balance}

    def issue_rewards(self, address: str, activity_value: float) -> str:
        """
        Issues reward tokens to a user's address based on activity value.
        :param address: The address to receive the rewards.
        :param activity_value: The value of the user's activity (e.g., stake amount or transaction volume).
        :return: Message indicating the reward issuance.
        """
        reward_amount = activity_value * self.reward_rate
        if self.current_supply + reward_amount > self.total_supply:
            return "Cannot issue rewards. Total supply limit reached."

        self.balances[address] = self.balances.get(address, 0) + reward_amount
        self.current_supply += reward_amount
        return f"Issued {reward_amount:.2f} {self.token_name} to {address}."

    def get_balance(self, address: str) -> float:
        """
        Gets the balance of reward tokens for a specific address.
        :param address: The address to check the balance for.
        :return: The balance of the address.
        """
        return self.balances.get(address, 0.0)

    def transfer(self, from_address: str, to_address: str, amount: float) -> str:
        """
        Transfers reward tokens from one address to another.
        :param from_address: The sender's address.
        :param to_address: The recipient's address.
        :param amount: The amount of tokens to transfer.
        :return: Message indicating the transfer result.
        """
        if from_address not in self.balances or self.balances[from_address] < amount:
            return "Insufficient balance to complete the transfer."

        self.balances[from_address] -= amount
        self.balances[to_address] = self.balances.get(to_address, 0) + amount
        return f"Transferred {amount:.2f} {self.token_name} from {from_address} to {to_address}."

    def get_total_supply(self) -> float:
        """
        Returns the current total supply of issued reward tokens.
        :return: The current total supply.
        """
        return self.current_supply


# Example usage
if __name__ == "__main__":
    # Initialize the reward token system
    reward_token = RewardToken(token_name="RewardCoin", total_supply=1000000, reward_rate=0.1)

    # Issue rewards
    print(reward_token.issue_rewards("address1", activity_value=500))
    print(reward_token.issue_rewards("address2", activity_value=300))

    # Check balances
    print(f"Balance of address1: {reward_token.get_balance('address1'):.2f}")
    print(f"Balance of address2: {reward_token.get_balance('address2'):.2f}")

    # Transfer tokens
    print(reward_token.transfer("address1", "address2", 20))

    # Check balances after transfer
    print(f"Balance of address1: {reward_token.get_balance('address1'):.2f}")
    print(f"Balance of address2: {reward_token.get_balance('address2'):.2f}")

    # Check total supply
    print(f"Current total supply: {reward_token.get_total_supply():.2f}")
