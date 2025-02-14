import hashlib
import time
from typing import Dict, Any


class ChannelSettlement:
    """Handles the settlement of state channels on the blockchain."""

    def __init__(self):
        self.channels = {}  # Stores active channels {channel_id: channel_data}
        self.settled_channels = {}  # Stores settled channels {channel_id: settlement_data}

    def open_channel(self, sender: str, receiver: str, initial_balance: float) -> str:
        """
        Opens a new state channel.
        :param sender: Address of the sender.
        :param receiver: Address of the receiver.
        :param initial_balance: Initial balance in the channel.
        :return: The unique channel ID.
        """
        if initial_balance <= 0:
            raise ValueError("Initial balance must be greater than zero.")

        channel_id = hashlib.sha256(f"{sender}{receiver}{time.time()}".encode()).hexdigest()
        self.channels[channel_id] = {
            "sender": sender,
            "receiver": receiver,
            "balance": initial_balance,
            "status": "open",
            "last_updated": time.time(),
        }
        print(f"Channel {channel_id} opened between {sender} and {receiver} with balance {initial_balance}.")
        return channel_id

    def close_channel(self, channel_id: str) -> bool:
        """
        Closes a state channel and prepares it for settlement.
        :param channel_id: The ID of the channel to close.
        :return: True if the channel is closed successfully, False otherwise.
        """
        channel = self.channels.get(channel_id)
        if not channel:
            print(f"Channel {channel_id} not found.")
            return False

        if channel["status"] != "open":
            print(f"Channel {channel_id} is already closed.")
            return False

        channel["status"] = "closed"
        channel["last_updated"] = time.time()
        print(f"Channel {channel_id} closed. Ready for settlement.")
        return True

    def settle_channel(self, channel_id: str, final_sender_balance: float, final_receiver_balance: float) -> bool:
        """
        Settles the state channel and transfers the final balances to participants.
        :param channel_id: The ID of the channel to settle.
        :param final_sender_balance: The final balance of the sender.
        :param final_receiver_balance: The final balance of the receiver.
        :return: True if the settlement is successful, False otherwise.
        """
        channel = self.channels.get(channel_id)
        if not channel:
            print(f"Channel {channel_id} not found.")
            return False

        if channel["status"] != "closed":
            print(f"Channel {channel_id} is not closed.")
            return False

        total_balance = final_sender_balance + final_receiver_balance
        if total_balance > channel["balance"]:
            print("Invalid settlement: Total balance exceeds initial channel balance.")
            return False

        # Record settlement data
        self.settled_channels[channel_id] = {
            "sender": channel["sender"],
            "receiver": channel["receiver"],
            "final_sender_balance": final_sender_balance,
            "final_receiver_balance": final_receiver_balance,
            "settled_at": time.time(),
        }

        # Remove channel from active list
        del self.channels[channel_id]
        print(f"Channel {channel_id} settled. Final balances - Sender: {final_sender_balance}, Receiver: {final_receiver_balance}.")
        return True

    def get_channel(self, channel_id: str) -> Dict[str, Any]:
        """
        Retrieves details of a specific channel.
        :param channel_id: The ID of the channel.
        :return: Channel details.
        """
        return self.channels.get(channel_id, {})

    def get_settled_channel(self, channel_id: str) -> Dict[str, Any]:
        """
        Retrieves details of a settled channel.
        :param channel_id: The ID of the settled channel.
        :return: Settled channel details.
        """
        return self.settled_channels.get(channel_id, {})


# Example usage
if __name__ == "__main__":
    manager = ChannelSettlement()

    # Open a new channel
    channel_id = manager.open_channel(sender="address1", receiver="address2", initial_balance=100.0)

    # Close the channel
    manager.close_channel(channel_id)

    # Settle the channel
    manager.settle_channel(channel_id, final_sender_balance=40.0, final_receiver_balance=60.0)

    # Retrieve settled channel details
    print("\nSettled Channel Details:")
    print(manager.get_settled_channel(channel_id))
