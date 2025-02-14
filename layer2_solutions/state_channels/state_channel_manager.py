import hashlib
import time
from typing import Dict, Any, List


class StateChannelManager:
    """Manages the lifecycle of state channels, including opening, updating, and closing channels."""

    def __init__(self):
        self.channels = {}  # Stores state channels {channel_id: channel_data}

    def open_channel(self, sender: str, receiver: str, initial_balance: float) -> str:
        """
        Opens a new state channel between a sender and receiver.
        :param sender: Address of the sender.
        :param receiver: Address of the receiver.
        :param initial_balance: Initial balance for the channel.
        :return: The unique channel ID.
        """
        if initial_balance <= 0:
            raise ValueError("Initial balance must be greater than zero.")

        channel_id = hashlib.sha256(f"{sender}{receiver}{time.time()}".encode()).hexdigest()
        self.channels[channel_id] = {
            "sender": sender,
            "receiver": receiver,
            "balance": initial_balance,
            "updated_at": time.time(),
            "status": "open",
            "transactions": []
        }
        print(f"State channel {channel_id} opened between {sender} and {receiver} with balance {initial_balance}.")
        return channel_id

    def update_channel(self, channel_id: str, sender: str, amount: float) -> bool:
        """
        Updates the state channel with a new transaction.
        :param channel_id: The ID of the channel.
        :param sender: The sender of the transaction.
        :param amount: The amount being transferred.
        :return: True if the update is successful, False otherwise.
        """
        channel = self.channels.get(channel_id)
        if not channel:
            print(f"Channel {channel_id} not found.")
            return False

        if channel["status"] != "open":
            print(f"Channel {channel_id} is not open.")
            return False

        if sender == channel["sender"]:
            if channel["balance"] < amount:
                print(f"Insufficient balance in channel {channel_id}.")
                return False
            channel["balance"] -= amount
        elif sender == channel["receiver"]:
            channel["balance"] += amount
        else:
            print("Invalid sender address.")
            return False

        channel["transactions"].append({
            "sender": sender,
            "amount": amount,
            "timestamp": time.time()
        })
        channel["updated_at"] = time.time()
        print(f"Channel {channel_id} updated. New balance: {channel['balance']}.")
        return True

    def close_channel(self, channel_id: str) -> bool:
        """
        Closes an existing state channel.
        :param channel_id: The ID of the channel to close.
        :return: True if the channel was closed, False otherwise.
        """
        channel = self.channels.get(channel_id)
        if not channel:
            print(f"Channel {channel_id} not found.")
            return False

        if channel["status"] != "open":
            print(f"Channel {channel_id} is already closed.")
            return False

        channel["status"] = "closed"
        channel["updated_at"] = time.time()
        print(f"Channel {channel_id} closed. Final balance: {channel['balance']}.")
        return True

    def get_channel(self, channel_id: str) -> Dict[str, Any]:
        """
        Retrieves details of a specific state channel.
        :param channel_id: The ID of the channel.
        :return: The channel details.
        """
        return self.channels.get(channel_id, {})

    def list_channels(self) -> List[Dict[str, Any]]:
        """
        Lists all state channels.
        :return: A list of state channel details.
        """
        return [{"channel_id": channel_id, **data} for channel_id, data in self.channels.items()]


# Example usage
if __name__ == "__main__":
    manager = StateChannelManager()

    # Open a new channel
    channel_id = manager.open_channel(sender="address1", receiver="address2", initial_balance=100.0)

    # Update the channel
    manager.update_channel(channel_id=channel_id, sender="address1", amount=20.0)
    manager.update_channel(channel_id=channel_id, sender="address2", amount=10.0)

    # List all channels
    print("\nAll Channels:")
    for channel in manager.list_channels():
        print(channel)

    # Close the channel
    manager.close_channel(channel_id)

    # Get specific channel details
    print("\nChannel Details:")
    print(manager.get_channel(channel_id))
