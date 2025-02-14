class CongestionBasedFees:
    """Adjusts transaction fees dynamically based on network congestion."""

    def __init__(self, base_fee: float, max_fee: float, congestion_threshold: int):
        """
        Initializes the CongestionBasedFees with the necessary parameters.
        :param base_fee: The base fee for transactions under normal conditions.
        :param max_fee: The maximum allowable fee during peak congestion.
        :param congestion_threshold: The percentage of mempool usage that triggers peak fees.
        """
        self.base_fee = base_fee
        self.max_fee = max_fee
        self.congestion_threshold = congestion_threshold

    def calculate(self, transaction_size: int, current_mempool_usage: int) -> float:
        """
        Calculates the transaction fee based on current network congestion.
        :param transaction_size: Size of the transaction in bytes.
        :param current_mempool_usage: Current mempool usage as a percentage (0-100).
        :return: The calculated transaction fee.
        """
        if current_mempool_usage >= self.congestion_threshold:
            # Peak congestion: Scale fee between base and max fee
            fee_per_byte = self._scale_fee(current_mempool_usage)
        else:
            # Normal conditions: Use base fee
            fee_per_byte = self.base_fee

        return fee_per_byte * transaction_size

    def _scale_fee(self, current_mempool_usage: int) -> float:
        """
        Scales the fee linearly between base_fee and max_fee based on congestion level.
        :param current_mempool_usage: Current mempool usage as a percentage.
        :return: Scaled fee per byte.
        """
        excess_usage = current_mempool_usage - self.congestion_threshold
        scale_factor = min(excess_usage / (100 - self.congestion_threshold), 1.0)
        return self.base_fee + (self.max_fee - self.base_fee) * scale_factor


# Example usage
if __name__ == "__main__":
    # Initialize with example parameters
    congestion_fees = CongestionBasedFees(base_fee=0.0001, max_fee=0.0010, congestion_threshold=80)

    # Example transaction size in bytes
    transaction_size = 250

    # Example current mempool usage (percentage)
    current_mempool_usage = 85  # 85% of the mempool is full

    # Calculate the transaction fee
    fee = congestion_fees.calculate(transaction_size, current_mempool_usage)
    print(f"Calculated Congestion-Based Fee: {fee:.8f} coins")
