class PegManager:
    """Manages the stability of the stablecoin peg."""

    def __init__(self, target_value: float, lower_bound: float, upper_bound: float, rebalance_rate: float):
        """
        Initializes the PegManager.
        :param target_value: The target value of the stablecoin (e.g., 1.0 for USD).
        :param lower_bound: The minimum value before intervention.
        :param upper_bound: The maximum value before intervention.
        :param rebalance_rate: Percentage of supply to adjust during rebalancing.
        """
        self.target_value = target_value
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.rebalance_rate = rebalance_rate

    def monitor_peg(self, current_value: float) -> str:
        """
        Monitors the current stablecoin value and determines if rebalancing is needed.
        :param current_value: The current value of the stablecoin.
        :return: A message indicating the action taken or that no action is needed.
        """
        if current_value < self.lower_bound:
            return self._mint_stablecoin()
        elif current_value > self.upper_bound:
            return self._burn_stablecoin()
        else:
            return "Stablecoin value is within acceptable range. No action needed."

    def _mint_stablecoin(self) -> str:
        """
        Mints new stablecoins to increase supply and restore the peg.
        :return: A message indicating that stablecoins have been minted.
        """
        adjustment = self.target_value * self.rebalance_rate
        # Simulate minting logic
        return f"Minted {adjustment:.2f} stablecoins to increase supply and restore the peg."

    def _burn_stablecoin(self) -> str:
        """
        Burns stablecoins to reduce supply and restore the peg.
        :return: A message indicating that stablecoins have been burned.
        """
        adjustment = self.target_value * self.rebalance_rate
        # Simulate burning logic
        return f"Burned {adjustment:.2f} stablecoins to reduce supply and restore the peg."


# Example usage
if __name__ == "__main__":
    # Initialize PegManager for a USD-pegged stablecoin
    peg_manager = PegManager(target_value=1.0, lower_bound=0.98, upper_bound=1.02, rebalance_rate=0.05)

    # Monitor and rebalance the peg based on the current value
    current_value = 0.97  # Example: stablecoin value below the lower bound
    print(peg_manager.monitor_peg(current_value))

    current_value = 1.03  # Example: stablecoin value above the upper bound
    print(peg_manager.monitor_peg(current_value))

    current_value = 1.00  # Example: stablecoin value within acceptable range
    print(peg_manager.monitor_peg(current_value))
