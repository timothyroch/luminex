from typing import List, Dict


class AuthorityManager:
    """Manages the list of authorized validators in a PoA sidechain."""

    def __init__(self):
        self.authorized_validators = {}  # Stores validators {validator_address: metadata}

    def add_validator(self, validator_address: str, metadata: Dict[str, str]) -> bool:
        """
        Adds a new validator to the authority list.
        :param validator_address: The address of the validator to add.
        :param metadata: Additional information about the validator (e.g., name, organization).
        :return: True if the validator was successfully added, False otherwise.
        """
        if validator_address in self.authorized_validators:
            print(f"Validator {validator_address} is already authorized.")
            return False

        self.authorized_validators[validator_address] = metadata
        print(f"Validator {validator_address} added with metadata: {metadata}.")
        return True

    def remove_validator(self, validator_address: str) -> bool:
        """
        Removes a validator from the authority list.
        :param validator_address: The address of the validator to remove.
        :return: True if the validator was successfully removed, False otherwise.
        """
        if validator_address not in self.authorized_validators:
            print(f"Validator {validator_address} is not authorized.")
            return False

        del self.authorized_validators[validator_address]
        print(f"Validator {validator_address} removed.")
        return True

    def is_validator_authorized(self, validator_address: str) -> bool:
        """
        Checks if a validator is authorized.
        :param validator_address: The address of the validator to check.
        :return: True if the validator is authorized, False otherwise.
        """
        return validator_address in self.authorized_validators

    def list_validators(self) -> List[Dict[str, str]]:
        """
        Lists all authorized validators and their metadata.
        :return: A list of validator metadata.
        """
        return [{"validator_address": addr, "metadata": meta} for addr, meta in self.authorized_validators.items()]

    def update_validator_metadata(self, validator_address: str, metadata: Dict[str, str]) -> bool:
        """
        Updates the metadata for a validator.
        :param validator_address: The address of the validator to update.
        :param metadata: The new metadata for the validator.
        :return: True if the metadata was successfully updated, False otherwise.
        """
        if validator_address not in self.authorized_validators:
            print(f"Validator {validator_address} is not authorized.")
            return False

        self.authorized_validators[validator_address] = metadata
        print(f"Metadata for validator {validator_address} updated to: {metadata}.")
        return True


# Example usage
if __name__ == "__main__":
    manager = AuthorityManager()

    # Add validators
    manager.add_validator("val1", {"name": "Validator 1", "organization": "Org1"})
    manager.add_validator("val2", {"name": "Validator 2", "organization": "Org2"})

    # List validators
    print("\nAuthorized Validators:")
    for validator in manager.list_validators():
        print(validator)

    # Check if a validator is authorized
    print("\nIs 'val1' authorized?", manager.is_validator_authorized("val1"))
    print("Is 'val3' authorized?", manager.is_validator_authorized("val3"))

    # Update validator metadata
    manager.update_validator_metadata("val1", {"name": "Validator One", "organization": "UpdatedOrg1"})

    # Remove a validator
    manager.remove_validator("val2")

    # List validators after removal
    print("\nAuthorized Validators after removal:")
    for validator in manager.list_validators():
        print(validator)
