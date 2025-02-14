import unittest
from cryptocurrency.fees.fee_calculator import FeeCalculator
from cryptocurrency.fees.static_fees import StaticFeeModel
from cryptocurrency.fees.congestion_based_fees import CongestionBasedFeeModel
from blockchain.transactions.transaction import Transaction

class TestFees(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing fee calculations.
        """
        self.static_fee_model = StaticFeeModel(fixed_fee=0.001)
        self.congestion_fee_model = CongestionBasedFeeModel(base_fee=0.0005, congestion_multiplier=2)
        self.fee_calculator = FeeCalculator(static_model=self.static_fee_model, dynamic_model=self.congestion_fee_model)

        # Sample transactions
        self.transaction_low_load = Transaction(
            sender="address1",
            recipient="address2",
            amount=10,
            timestamp=1673367600,
            signature="VALID_SIGNATURE"
        )
        self.transaction_high_load = Transaction(
            sender="address3",
            recipient="address4",
            amount=20,
            timestamp=1673368600,
            signature="VALID_SIGNATURE"
        )

    def test_static_fee(self):
        """
        Test that the static fee model calculates the correct fee.
        """
        fee = self.static_fee_model.calculate_fee(self.transaction_low_load)
        self.assertEqual(fee, 0.001, "Static fee calculation is incorrect")
        print("Static fee test passed.")

    def test_congestion_based_fee_low_load(self):
        """
        Test that the congestion-based fee model calculates the correct fee under low network load.
        """
        fee = self.congestion_fee_model.calculate_fee(self.transaction_low_load, network_load=10)
        self.assertEqual(fee, 0.0005, "Congestion-based fee calculation under low load is incorrect")
        print("Congestion-based fee (low load) test passed.")

    def test_congestion_based_fee_high_load(self):
        """
        Test that the congestion-based fee model calculates the correct fee under high network load.
        """
        fee = self.congestion_fee_model.calculate_fee(self.transaction_high_load, network_load=90)
        self.assertEqual(fee, 0.001, "Congestion-based fee calculation under high load is incorrect")
        print("Congestion-based fee (high load) test passed.")

    def test_fee_calculator_static(self):
        """
        Test that the fee calculator uses the static fee model correctly.
        """
        fee = self.fee_calculator.calculate_fee(self.transaction_low_load, use_dynamic=False)
        self.assertEqual(fee, 0.001, "Fee calculator failed to use the static fee model correctly")
        print("Fee calculator (static model) test passed.")

    def test_fee_calculator_dynamic(self):
        """
        Test that the fee calculator uses the dynamic (congestion-based) fee model correctly.
        """
        fee = self.fee_calculator.calculate_fee(self.transaction_high_load, use_dynamic=True, network_load=90)
        self.assertEqual(fee, 0.001, "Fee calculator failed to use the dynamic fee model correctly")
        print("Fee calculator (dynamic model) test passed.")

if __name__ == "__main__":
    unittest.main()
