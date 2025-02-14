import json
from typing import Dict, List

class BalanceTracker:
    """Tracks wallet balances across multiple accounts by scanning blockchain transactions."""

    def __init__(self):
        self.balances = {}  # Stores balances in the format: {address: balance}

    def update_balance(self, address: str, amount: float):
        """
        Updates the balance of a given address.
        :param address: The wallet address to update.
        :param amount: The amount to add or subtract from the balance.
        """
        if address not in self.balances:
            self.balances[address] = 0.0
        self.balances[address] += amount

    def process_transaction(self, transaction: Dict):
        """
        Processes a single transaction and updates balances for the sender and receiver.
        :param transaction: A dictionary representing the transaction with keys:
                            - sender: the sender's address
                            - receiver: the receiver's address
                            - amount: the amount transferred
        """
        sender = transaction.get("sender")
        receiver = transaction.get("receiver")
        amount = transaction.get("amount")

        if sender and receiver and amount is not None:
            # Deduct from sender
            self.update_balance(sender, -amount)
            # Add to receiver
            self.update_balance(receiver, amount)
        else:
            raise ValueError("Invalid transaction format. Must include sender, receiver, and amount.")

    def process_block(self, block: Dict):
        """
        Processes all transactions in a block to update balances.
        :param block: A dictionary representing the block with a "transactions" key.
        """
        transactions = block.get("transactions", [])
        for transaction in transactions:
            self.process_transaction(transaction)

    def get_balance(self, address: str) -> float:
        """
        Returns the current balance of a given address.
        :param address: The wallet address to query.
        :return: The balance of the address.
        """
        return self.balances.get(address, 0.0)

    def load_balances(self, file_path: str):
        """
        Loads previously saved balances from a JSON file.
        :param file_path: The path to the JSON file containing balance data.
        """
        try:
            with open(file_path, "r") as file:
                self.balances = json.load(file)
        except FileNotFoundError:
            print(f"No balance file found at {file_path}. Starting with empty balances.")

    def save_balances(self, file_path: str):
        """
        Saves the current balances to a JSON file.
        :param file_path: The path to the JSON file for saving balance data.
        """
        with open(file_path, "w") as file:
            json.dump(self.balances, file, indent=4)
        print(f"Balances saved to {file_path}.")


# Example usage
if __name__ == "__main__":
    tracker = BalanceTracker()

    # Example block with transactions
    block = {
        "transactions": [
            {"sender": "Alice", "receiver": "Bob", "amount": 50},
            {"sender": "Bob", "receiver": "Charlie", "amount": 30},
            {"sender": "Alice", "receiver": "Charlie", "amount": 20}
        ]
    }

    # Process the block
    tracker.process_block(block)

    # Get balances
    print("Balance of Alice:", tracker.get_balance("Alice"))
    print("Balance of Bob:", tracker.get_balance("Bob"))
    print("Balance of Charlie:", tracker.get_balance("Charlie"))

    # Save balances to a file
    tracker.save_balances("balances.json")

    # Load balances from the file
    tracker.load_balances("balances.json")
    print("Loaded Balances:", tracker.balances)
