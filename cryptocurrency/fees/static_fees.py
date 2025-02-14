class StaticFees:
    """Implements a fixed-fee model for transactions."""

    def __init__(self, base_fee: float):
        """
        Initializes the StaticFees with a base fee.
        :param base_fee: Fixed fee per byte for transactions.
        """
        self.base_fee = base_fee

    def calculate(self, transaction_size: int) -> float:
        """
        Calculates the transaction fee using a fixed-fee model.
        :param transaction_size: Size of the transaction in bytes.
        :return: The calculated transaction fee.
        """
        if transaction_size <= 0:
            raise ValueError("Transaction size must be a positive integer.")
        return self.base_fee * transaction_size


# Example usage
if __name__ == "__main__":
    # Initialize with example base fee
    static_fees = StaticFees(base_fee=0.0001)

    # Example transaction size in bytes
    transaction_size = 300

    # Calculate the transaction fee
    fee = static_fees.calculate(transaction_size)
    print(f"Calculated Static Fee: {fee:.8f} coins")
