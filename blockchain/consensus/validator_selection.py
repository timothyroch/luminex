import random
import json

class ValidatorSelection:
    """Handles the process of selecting a validator based on stake-weighted random selection."""

    def __init__(self, config_file="blockchain/consensus/consensus_config.json"):
        """
        Initializes the ValidatorSelection class by loading configuration and validator stakes.
        :param config_file: Path to the JSON configuration file.
        """
        with open(config_file) as file:
            self.config = json.load(file)
        self.minimum_stake = self.config["minimum_stake"]
        self.max_validator_count = self.config["max_validator_count"]
        self.rotation_policy = self.config["validator_rotation_policy"]
        self.validators = {}  # Format: {validator_id: stake}
        self.current_index = 0  # Used for round-robin rotation

    def add_validator(self, validator_id, stake):
        """
        Adds a validator to the selection pool.
        :param validator_id: The unique identifier of the validator.
        :param stake: The amount of stake the validator has.
        """
        if len(self.validators) >= self.max_validator_count:
            raise Exception("Max validator count reached.")
        if stake < self.minimum_stake:
            raise Exception(f"Validator {validator_id} does not meet the minimum stake requirement.")
        self.validators[validator_id] = stake

    def remove_validator(self, validator_id):
        """
        Removes a validator from the selection pool.
        :param validator_id: The unique identifier of the validator.
        """
        if validator_id in self.validators:
            del self.validators[validator_id]

    def select_validator(self):
        """
        Selects a validator based on the configured rotation policy.
        :return: The selected validator's ID.
        """
        if self.rotation_policy == "round_robin":
            return self._round_robin_selection()
        else:
            return self._stake_weighted_selection()

    def _round_robin_selection(self):
        """Implements round-robin validator selection."""
        if not self.validators:
            raise Exception("No validators available for selection.")
        validator_ids = list(self.validators.keys())
        selected = validator_ids[self.current_index]
        self.current_index = (self.current_index + 1) % len(validator_ids)
        return selected

    def _stake_weighted_selection(self):
        """Implements stake-weighted random validator selection."""
        if not self.validators:
            raise Exception("No validators available for selection.")
        total_stake = sum(self.validators.values())
        validators = list(self.validators.keys())
        weights = [self.validators[v] / total_stake for v in validators]
        selected = random.choices(validators, weights=weights, k=1)[0]
        return selected

    def get_validators(self):
        """
        Returns the current list of validators and their stakes.
        :return: A dictionary of {validator_id: stake}.
        """
        return self.validators


# Example usage
if __name__ == "__main__":
    selection = ValidatorSelection()

    # Add validators
    selection.add_validator("Validator1", 5000)
    selection.add_validator("Validator2", 3000)
    selection.add_validator("Validator3", 2000)

    # Select validators
    print(f"Selected Validator (Round Robin): {selection.select_validator()}")
    print(f"Selected Validator (Stake Weighted): {selection.select_validator()}")

    # Remove a validator and print the updated list
    selection.remove_validator("Validator2")
    print("Updated Validators:", selection.get_validators())
