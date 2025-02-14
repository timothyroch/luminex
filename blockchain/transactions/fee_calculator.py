class FeeCalculator:
    """Calculates transaction fees using different fee models."""

    def __init__(self, base_fee=1, dynamic_fee_rate=0.01, congestion_threshold=1000):
        """
        Initializes the FeeCalculator.
        :param base_fee: The static base fee for all transactions.
        :param dynamic_fee_rate: The dynamic fee rate (percentage of transaction amount).
        :param congestion_threshold: Number of pending transactions that triggers congestion pricing.
        """
        self.base_fee = base_fee
        self.dynamic_fee_rate = dynamic_fee_rate
        self.congestion_threshold = congestion_threshold

    def calculate_static_fee(self):
        """
        Calculates the static fee.
        :return: The static fee.
        """
        return self.base_fee

    def calculate_dynamic_fee(self, transaction_amount):
        """
        Calculates the dynamic fee based on transaction amount.
        :param transaction_amount: The amount of the transaction.
        :return: The dynamic fee.
        """
        return transaction_amount * self.dynamic_fee_rate

    def calculate_congestion_fee(self, pending_transactions):
        """
        Calculates an additional congestion fee if the transaction pool exceeds the congestion threshold.
        :param pending_transactions: The current number of pending transactions.
        :return: The congestion fee.
        """
        if pending_transactions > self.congestion_threshold:
            return self.base_fee * 2  # Double the base fee as congestion penalty
        return 0

    def calculate_total_fee(self, transaction_amount, pending_transactions):
        """
        Calculates the total fee for a transaction.
        :param transaction_amount: The amount of the transaction.
        :param pending_transactions: The current number of pending transactions in the pool.
        :return: The total transaction fee.
        """
        static_fee = self.calculate_static_fee()
        dynamic_fee = self.calculate_dynamic_fee(transaction_amount)
        congestion_fee = self.calculate_congestion_fee(pending_transactions)

        total_fee = static_fee + dynamic_fee + congestion_fee
        return total_fee


# Example usage
if __name__ == "__main__":
    # Initialize the FeeCalculator
    fee_calculator = FeeCalculator(base_fee=1, dynamic_fee_rate=0.01, congestion_threshold=1000)

    # Simulate a transaction
    transaction_amount = 200  # Transaction amount in blockchain units
    pending_transactions = 1200  # Number of transactions in the pool

    # Calculate the total fee
    total_fee = fee_calculator.calculate_total_fee(transaction_amount, pending_transactions)
    print("Total Transaction Fee:", total_fee)
