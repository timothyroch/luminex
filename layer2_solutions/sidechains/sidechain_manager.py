import time
from typing import Dict, List, Any


class SidechainManager:
    """Manages the creation, maintenance, and lifecycle of sidechains."""

    def __init__(self):
        self.sidechains = {}  # Stores sidechains {chain_id: sidechain_data}
        self.next_chain_id = 1  # Incremental ID for new sidechains

    def create_sidechain(self, name: str, consensus: str, initial_validators: List[str]) -> Dict[str, Any]:
        """
        Creates a new sidechain.
        :param name: The name of the sidechain.
        :param consensus: The consensus mechanism used (e.g., PoA, PoS).
        :param initial_validators: A list of initial validator addresses.
        :return: The created sidechain data.
        """
        chain_id = self.next_chain_id
        self.next_chain_id += 1

        sidechain_data = {
            "chain_id": chain_id,
            "name": name,
            "consensus": consensus,
            "validators": initial_validators,
            "created_at": time.time(),
            "active": True,
        }

        self.sidechains[chain_id] = sidechain_data
        print(f"Sidechain '{name}' created with chain ID {chain_id}.")
        return sidechain_data

    def deactivate_sidechain(self, chain_id: int) -> bool:
        """
        Deactivates a sidechain.
        :param chain_id: The ID of the sidechain to deactivate.
        :return: True if the sidechain was successfully deactivated, False otherwise.
        """
        sidechain = self.sidechains.get(chain_id)
        if not sidechain:
            print(f"Sidechain with chain ID {chain_id} not found.")
            return False

        sidechain["active"] = False
        print(f"Sidechain with chain ID {chain_id} has been deactivated.")
        return True

    def list_sidechains(self) -> List[Dict[str, Any]]:
        """
        Lists all sidechains.
        :return: A list of sidechain data.
        """
        return list(self.sidechains.values())

    def get_sidechain(self, chain_id: int) -> Dict[str, Any]:
        """
        Retrieves a specific sidechain's data.
        :param chain_id: The ID of the sidechain to retrieve.
        :return: The sidechain data.
        """
        sidechain = self.sidechains.get(chain_id)
        if not sidechain:
            print(f"Sidechain with chain ID {chain_id} not found.")
            return {}
        return sidechain

    def add_validator(self, chain_id: int, validator_address: str) -> bool:
        """
        Adds a new validator to a sidechain.
        :param chain_id: The ID of the sidechain.
        :param validator_address: The address of the new validator.
        :return: True if the validator was added, False otherwise.
        """
        sidechain = self.sidechains.get(chain_id)
        if not sidechain:
            print(f"Sidechain with chain ID {chain_id} not found.")
            return False

        if validator_address in sidechain["validators"]:
            print(f"Validator {validator_address} is already part of the sidechain.")
            return False

        sidechain["validators"].append(validator_address)
        print(f"Validator {validator_address} added to sidechain {chain_id}.")
        return True

    def remove_validator(self, chain_id: int, validator_address: str) -> bool:
        """
        Removes a validator from a sidechain.
        :param chain_id: The ID of the sidechain.
        :param validator_address: The address of the validator to remove.
        :return: True if the validator was removed, False otherwise.
        """
        sidechain = self.sidechains.get(chain_id)
        if not sidechain:
            print(f"Sidechain with chain ID {chain_id} not found.")
            return False

        if validator_address not in sidechain["validators"]:
            print(f"Validator {validator_address} is not part of the sidechain.")
            return False

        sidechain["validators"].remove(validator_address)
        print(f"Validator {validator_address} removed from sidechain {chain_id}.")
        return True


# Example usage
if __name__ == "__main__":
    manager = SidechainManager()

    # Create a sidechain
    sidechain1 = manager.create_sidechain(name="TestChain1", consensus="PoA", initial_validators=["val1", "val2"])
    print("Created Sidechain:", sidechain1)

    # Add a validator
    manager.add_validator(chain_id=1, validator_address="val3")

    # Remove a validator
    manager.remove_validator(chain_id=1, validator_address="val1")

    # List all sidechains
    print("\nAll Sidechains:", manager.list_sidechains())

    # Get details of a specific sidechain
    print("\nDetails of Sidechain 1:", manager.get_sidechain(chain_id=1))

    # Deactivate a sidechain
    manager.deactivate_sidechain(chain_id=1)
