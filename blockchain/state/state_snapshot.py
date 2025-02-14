import json
import os
import shutil
import time

class StateSnapshot:
    """Manages blockchain state snapshots for recovery and synchronization."""

    def __init__(self, snapshot_dir="blockchain/state/snapshots"):
        """
        Initializes the StateSnapshot.
        :param snapshot_dir: Directory where snapshots are stored.
        """
        self.snapshot_dir = snapshot_dir
        os.makedirs(self.snapshot_dir, exist_ok=True)

    def create_snapshot(self, state, block_height):
        """
        Creates a snapshot of the current blockchain state.
        :param state: The current global state to snapshot (dict format).
        :param block_height: The block height at which the snapshot is taken.
        :return: The file path of the created snapshot.
        """
        snapshot_file = os.path.join(self.snapshot_dir, f"snapshot_{block_height}.json")
        with open(snapshot_file, "w") as file:
            json.dump(state, file, indent=4)
        print(f"Snapshot created at block height {block_height}: {snapshot_file}")
        return snapshot_file

    def load_snapshot(self, block_height):
        """
        Loads a snapshot for a given block height.
        :param block_height: The block height of the desired snapshot.
        :return: The loaded state (dict format).
        """
        snapshot_file = os.path.join(self.snapshot_dir, f"snapshot_{block_height}.json")
        if not os.path.exists(snapshot_file):
            raise FileNotFoundError(f"Snapshot for block height {block_height} not found.")
        with open(snapshot_file, "r") as file:
            state = json.load(file)
        print(f"Loaded snapshot from block height {block_height}.")
        return state

    def cleanup_old_snapshots(self, keep_last_n=5):
        """
        Removes old snapshots, keeping only the latest `n` snapshots.
        :param keep_last_n: Number of recent snapshots to keep.
        """
        snapshots = sorted(
            [f for f in os.listdir(self.snapshot_dir) if f.startswith("snapshot_")],
            key=lambda x: int(x.split("_")[1].split(".")[0])
        )

        if len(snapshots) > keep_last_n:
            for old_snapshot in snapshots[:-keep_last_n]:
                os.remove(os.path.join(self.snapshot_dir, old_snapshot))
            print(f"Cleaned up old snapshots, keeping the last {keep_last_n}.")
        else:
            print("No old snapshots to clean up.")

    def get_latest_snapshot(self):
        """
        Retrieves the latest available snapshot.
        :return: The file path of the latest snapshot and its block height.
        """
        snapshots = sorted(
            [f for f in os.listdir(self.snapshot_dir) if f.startswith("snapshot_")],
            key=lambda x: int(x.split("_")[1].split(".")[0])
        )
        if not snapshots:
            raise FileNotFoundError("No snapshots found.")
        latest_snapshot = snapshots[-1]
        block_height = int(latest_snapshot.split("_")[1].split(".")[0])
        return os.path.join(self.snapshot_dir, latest_snapshot), block_height

    def rollback_to_snapshot(self, block_height, state_manager):
        """
        Rolls back the blockchain state to a specified snapshot.
        :param block_height: The block height of the snapshot to roll back to.
        :param state_manager: The StateManager instance to update the global state.
        """
        snapshot = self.load_snapshot(block_height)
        state_manager.state = snapshot
        state_manager.utxo_set = snapshot["utxo_set"]
        state_manager.balances = snapshot["balances"]
        state_manager.nonces = snapshot["nonces"]
        state_manager.smart_contract_engine.contracts = snapshot["smart_contracts"]
        print(f"Rolled back to snapshot at block height {block_height}.")

# Example usage
if __name__ == "__main__":
    # Mock state data for demonstration
    mock_state = {
        "balances": {"Alice": 100, "Bob": 50},
        "nonces": {"Alice": 1, "Bob": 0},
        "utxo_set": {
            ("tx1", 0): {"receiver": "Alice", "amount": 50},
            ("tx1", 1): {"receiver": "Bob", "amount": 30}
        },
        "smart_contracts": {
            "contract1": {
                "creator": "Alice",
                "state": {"token_balance": 1000}
            }
        }
    }

    snapshot_manager = StateSnapshot()

    # Create a snapshot at block height 10
    snapshot_manager.create_snapshot(mock_state, 10)

    # Load the snapshot
    loaded_state = snapshot_manager.load_snapshot(10)
    print("Loaded State:", loaded_state)

    # Create another snapshot at block height 20
    snapshot_manager.create_snapshot(mock_state, 20)

    # Cleanup old snapshots, keeping only the last 1
    snapshot_manager.cleanup_old_snapshots(keep_last_n=1)

    # Get the latest snapshot
    latest_snapshot, height = snapshot_manager.get_latest_snapshot()
    print(f"Latest Snapshot: {latest_snapshot} (Block Height: {height})")
