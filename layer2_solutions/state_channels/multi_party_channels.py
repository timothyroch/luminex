import hashlib
import time
from typing import List, Dict, Any


class MultiPartyChannelManager:
    """Manages multi-party state channels, including opening, updating, and closing channels."""

    def __init__(self):
        self.channels = {}  # Stores multi-party channels {channel_id: channel_data}

    def open_channel(self, participants: List[str], initial_balances: List[float]) -> str:
        """
        Opens a new multi-party state channel.
        :param participants: List of participant addresses.
        :param initial_balances: List of initial balances corresponding to each participant.
        :return: The unique channel ID.
        """
        if len(participants) != len(initial_balances):
            raise ValueError("Participants and balances must have the same length.")

        if any(balance <= 0 for balance in initial_balances):
            raise ValueError("All initial balances must be greater than zero.")

        channel_id = hashlib.sha256(f"{participants}{time.time()}".encode()).hexdigest()
        self.channels[channel_id] = {
            "participants": participants,
            "balances": initial_balances,
            "status": "open",
            "transactions": [],
            "last_updated": time.time(),
        }
        print(f"Multi-party channel {channel_id} opened with participants {participants} and balances {initial_balances}.")
        return channel_id

    def update_channel(self, channel_id: str, sender: str, receiver: str, amount: float) -> bool:
        """
        Updates the state of a multi-party channel with a new transaction.
        :param channel_id: The ID of the channel to update.
        :param sender: The sender's address.
        :param receiver: The receiver's address.
        :param amount: The amount to transfer.
        :return: True if the update is successful, False otherwise.
        """
        channel = self.channels.get(channel_id)
        if not channel:
            print(f"Channel {channel_id} not found.")
            return False

        if channel["status"] != "open":
            print(f"Channel {channel_id} is not open.")
            return False

        participants = channel["participants"]
        if sender not in participants or receiver not in participants:
            print("Sender or receiver not part of the channel.")
            return False

        sender_index = participants.index(sender)
        receiver_index = participants.index(receiver)

        if channel["balances"][sender_index] < amount:
            print(f"Insufficient balance for sender {sender}.")
            return False

        # Update balances
        channel["balances"][sender_index] -= amount
        channel["balances"][receiver_index] += amount

        # Record transaction
        channel["transactions"].append({
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "timestamp": time.time(),
        })
        channel["last_updated"] = time.time()

        print(f"Channel {channel_id} updated. Balances: {channel['balances']}")
        return True

    def close_channel(self, channel_id: str) -> bool:
        """
        Closes a multi-party state channel.
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
        print(f"Channel {channel_id} closed. Final balances: {channel['balances']}")
        return True

    def get_channel(self, channel_id: str) -> Dict[str, Any]:
        """
        Retrieves details of a specific multi-party state channel.
        :param channel_id: The ID of the channel.
        :return: The channel details.
        """
        return self.channels.get(channel_id, {})

    def list_channels(self) -> List[Dict[str, Any]]:
        """
        Lists all multi-party state channels.
        :return: A list of state channel details.
        """
        return [{"channel_id": channel_id, **data} for channel_id, data in self.channels.items()]


# Example usage
if __name__ == "__main__":
    manager = MultiPartyChannelManager()

    # Open a new multi-party channel
    channel_id = manager.open_channel(
        participants=["address1", "address2", "address3"],
        initial_balances=[100.0, 50.0, 25.0]
    )

    # Update the channel
    manager.update_channel(channel_id=channel_id, sender="address1", receiver="address2", amount=20.0)
    manager.update_channel(channel_id=channel_id, sender="address3", receiver="address1", amount=10.0)

    # List all channels
    print("\nAll Channels:")
    for channel in manager.list_channels():
        print(channel)

    # Close the channel
    manager.close_channel(channel_id)

    # Get specific channel details
    print("\nChannel Details:")
    print(manager.get_channel(channel_id))
