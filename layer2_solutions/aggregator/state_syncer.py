import time
from typing import Dict, Any, List


class StateSyncer:
    """Synchronizes state between Layer 1 and Layer 2 solutions."""

    def __init__(self):
        self.layer1_state = {}  # Stores the state from Layer 1
        self.layer2_states = {}  # Stores the states of Layer 2 solutions {solution_type: state}

    def sync_from_layer1(self, state_data: Dict[str, Any]):
        """
        Synchronizes state from Layer 1 to the syncer.
        :param state_data: The state data from Layer 1.
        """
        self.layer1_state = state_data
        print(f"State synced from Layer 1: {state_data}")

    def sync_to_layer2(self, solution_type: str, state_data: Dict[str, Any]):
        """
        Synchronizes state from the syncer to a specific Layer 2 solution.
        :param solution_type: The type of Layer 2 solution (e.g., 'zk_rollups', 'sidechains').
        :param state_data: The state data to synchronize.
        """
        self.layer2_states[solution_type] = state_data
        print(f"State synced to {solution_type}: {state_data}")

    def fetch_layer1_state(self) -> Dict[str, Any]:
        """
        Retrieves the latest state from Layer 1.
        :return: The Layer 1 state.
        """
        print("Fetching state from Layer 1...")
        return self.layer1_state

    def fetch_layer2_state(self, solution_type: str) -> Dict[str, Any]:
        """
        Retrieves the latest state of a specific Layer 2 solution.
        :param solution_type: The type of Layer 2 solution.
        :return: The Layer 2 state.
        """
        print(f"Fetching state from {solution_type}...")
        return self.layer2_states.get(solution_type, {})

    def verify_state_consistency(self, solution_type: str) -> bool:
        """
        Verifies the consistency of state between Layer 1 and a specific Layer 2 solution.
        :param solution_type: The type of Layer 2 solution.
        :return: True if the states are consistent, False otherwise.
        """
        layer1_state = self.fetch_layer1_state()
        layer2_state = self.fetch_layer2_state(solution_type)

        # Simple consistency check for demonstration purposes
        consistent = layer1_state.get("balances") == layer2_state.get("balances")
        print(f"State consistency between Layer 1 and {solution_type}: {'consistent' if consistent else 'inconsistent'}")
        return consistent


# Example usage
if __name__ == "__main__":
    syncer = StateSyncer()

    # Mock Layer 1 state
    layer1_state = {
        "balances": {"address1": 100, "address2": 200},
        "last_block": 1500,
        "timestamp": time.time(),
    }
    syncer.sync_from_layer1(layer1_state)

    # Mock Layer 2 state for zk-rollups
    zk_rollups_state = {
        "balances": {"address1": 100, "address2": 200},
        "last_rollup_batch": 50,
        "timestamp": time.time(),
    }
    syncer.sync_to_layer2("zk_rollups", zk_rollups_state)

    # Verify state consistency
    syncer.verify_state_consistency("zk_rollups")

    # Fetch and display state
    print("\nLayer 1 State:", syncer.fetch_layer1_state())
    print("Layer 2 State (zk_rollups):", syncer.fetch_layer2_state("zk_rollups"))
