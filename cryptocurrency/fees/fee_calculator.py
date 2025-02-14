import json
from congestion_based_fees import CongestionBasedFees
from static_fees import StaticFees

class FeeCalculator:
    """Computes transaction fees dynamically based on configuration and network conditions."""

    def __init__(self, config_file="fee_config.json"):
        """
        Initializes the FeeCalculator with a configuration file.
        :param config_file: Path to the fee configuration file.
        """
        self.config = self.load_config(config_file)
        self.static_fees = StaticFees(self.config["static_base_fee"])
        self.congestion_fees = CongestionBasedFees(
            base_fee=self.config["congestion"]["base_fee"],
            max_fee=self.config["congestion"]["max_fee"],
            congestion_threshold=self.config["congestion"]["threshold"]
        )
        self.use_congestion_based = self.config["use_congestion_based"]

    def load_config(self, config_file):
        """
        Loads the fee configuration file.
        :param config_file: Path to the fee configuration file.
        :return: Parsed configuration as a dictionary.
        """
        with open(config_file, "r") as file:
            return json.load(file)

    def calculate_fee(self, transaction_size, current_mempool_usage):
        """
        Calculates the transaction fee based on the current fee model.
        :param transaction_size: Size of the transaction in bytes.
        :param current_mempool_usage: Current mempool usage as a percentage (0-100).
        :return: Calculated fee for the transaction.
        """
        if self.use_congestion_based:
            return self.congestion_fees.calculate(transaction_size, current_mempool_usage)
        else:
            return self.static_fees.calculate(transaction_size)


# Example usage
if __name__ == "__main__":
    # Example config file path
    config_path = "fee_config.json"

    # Initialize the FeeCalculator
    fee_calculator = FeeCalculator(config_file=config_path)

    # Example transaction size in bytes
    transaction_size = 250

    # Example current mempool usage (percentage)
    current_mempool_usage = 75  # 75% of the mempool is full

    # Calculate the transaction fee
    fee = fee_calculator.calculate_fee(transaction_size, current_mempool_usage)
    print(f"Calculated Fee: {fee:.8f} coins")
