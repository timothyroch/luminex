import time
from typing import Dict, List, Any


class PlasmaExitManager:
    """Manages the exit process from the Plasma sidechain to Layer 1."""

    def __init__(self):
        self.exit_queue = []  # Stores pending exits
        self.completed_exits = []  # Stores completed exits

    def request_exit(self, user_address: str, amount: float, block_number: int) -> Dict[str, Any]:
        """
        Requests an exit from the Plasma sidechain.
        :param user_address: The address of the user requesting the exit.
        :param amount: The amount to withdraw.
        :param block_number: The block number from which the exit is requested.
        :return: Exit request data.
        """
        if amount <= 0:
            raise ValueError("Exit amount must be greater than zero.")

        exit_request = {
            "user_address": user_address,
            "amount": amount,
            "block_number": block_number,
            "timestamp": time.time(),
            "status": "pending"
        }
        self.exit_queue.append(exit_request)
        print(f"Exit requested by {user_address} for amount {amount} from block {block_number}.")
        return exit_request

    def process_exit(self) -> bool:
        """
        Processes the oldest exit request in the queue.
        :return: True if an exit is processed, False otherwise.
        """
        if not self.exit_queue:
            print("No pending exits to process.")
            return False

        exit_request = self.exit_queue.pop(0)  # Remove the oldest exit request
        exit_request["status"] = "completed"
        exit_request["processed_at"] = time.time()
        self.completed_exits.append(exit_request)

        print(f"Exit processed for {exit_request['user_address']} from block {exit_request['block_number']} with amount {exit_request['amount']}.")
        return True

    def list_pending_exits(self) -> List[Dict[str, Any]]:
        """
        Lists all pending exit requests.
        :return: A list of pending exits.
        """
        return self.exit_queue

    def list_completed_exits(self) -> List[Dict[str, Any]]:
        """
        Lists all completed exit requests.
        :return: A list of completed exits.
        """
        return self.completed_exits

    def verify_exit(self, user_address: str, block_number: int) -> bool:
        """
        Verifies whether an exit is valid based on the provided user address and block number.
        :param user_address: The address of the user.
        :param block_number: The block number.
        :return: True if the exit is valid, False otherwise.
        """
        for exit_request in self.completed_exits:
            if exit_request["user_address"] == user_address and exit_request["block_number"] == block_number:
                print(f"Exit verified for {user_address} from block {block_number}.")
                return True

        print(f"No completed exit found for {user_address} from block {block_number}.")
        return False


# Example usage
if __name__ == "__main__":
    plasma_exit_manager = PlasmaExitManager()

    # Request exits
    plasma_exit_manager.request_exit(user_address="address1", amount=50.0, block_number=1)
    plasma_exit_manager.request_exit(user_address="address2", amount=100.0, block_number=2)

    # List pending exits
    print("\nPending Exits:")
    for exit_request in plasma_exit_manager.list_pending_exits():
        print(exit_request)

    # Process exits
    print("\nProcessing Exits:")
    plasma_exit_manager.process_exit()
    plasma_exit_manager.process_exit()

    # List completed exits
    print("\nCompleted Exits:")
    for completed_exit in plasma_exit_manager.list_completed_exits():
        print(completed_exit)

    # Verify an exit
    print("\nVerifying Exit:")
    plasma_exit_manager.verify_exit(user_address="address1", block_number=1)
