import json

class SlashingRules:
    """Handles penalties for malicious or faulty validators."""

    def __init__(self, config_file="blockchain/consensus/consensus_config.json"):
        """
        Initializes the SlashingRules class by loading configuration.
        :param config_file: Path to the JSON configuration file.
        """
        with open(config_file) as file:
            self.config = json.load(file)
        self.slashing_penalty = self.config["slashing_penalty"]
        self.downtime_threshold = self.config["malicious_behavior_detection"]["downtime_threshold_seconds"]
        self.double_signing_penalty = self.slashing_penalty * 2  # Example: harsher penalty for double-signing

    def slash_for_double_signing(self, validator, stakes):
        """
        Penalizes a validator for double-signing.
        :param validator: The ID of the validator to penalize.
        :param stakes: A dictionary of {validator: stake} pairs.
        :return: Updated stakes after slashing.
        """
        if validator not in stakes:
            raise Exception(f"Validator {validator} not found.")
        penalty = stakes[validator] * self.double_signing_penalty
        stakes[validator] -= penalty
        self.log_slashing_event(validator, "double_signing", penalty)
        return stakes

    def slash_for_downtime(self, validator, stakes, downtime_seconds):
        """
        Penalizes a validator for exceeding the downtime threshold.
        :param validator: The ID of the validator to penalize.
        :param stakes: A dictionary of {validator: stake} pairs.
        :param downtime_seconds: The number of seconds the validator was offline.
        :return: Updated stakes after slashing.
        """
        if validator not in stakes:
            raise Exception(f"Validator {validator} not found.")
        if downtime_seconds > self.downtime_threshold:
            penalty = stakes[validator] * self.slashing_penalty
            stakes[validator] -= penalty
            self.log_slashing_event(validator, "downtime", penalty)
        return stakes

    def log_slashing_event(self, validator, reason, penalty):
        """
        Logs slashing events for auditing and monitoring.
        :param validator: The ID of the slashed validator.
        :param reason: Reason for the slashing (e.g., 'double_signing', 'downtime').
        :param penalty: The amount of stake slashed.
        """
        with open("monitoring/logs/slashing_events.log", "a") as log_file:
            log_file.write(
                f"Validator: {validator}, Reason: {reason}, Penalty: {penalty:.2f}\n"
            )
        print(f"Validator {validator} slashed for {reason}. Penalty: {penalty:.2f}")

# Example usage
if __name__ == "__main__":
    stakes = {"Validator1": 5000, "Validator2": 3000, "Validator3": 2000}
    slashing = SlashingRules()

    # Example: Slash for double-signing
    print("Before double-signing slashing:", stakes)
    updated_stakes = slashing.slash_for_double_signing("Validator1", stakes)
    print("After double-signing slashing:", updated_stakes)

    # Example: Slash for downtime
    print("Before downtime slashing:", updated_stakes)
    updated_stakes = slashing.slash_for_downtime("Validator2", updated_stakes, downtime_seconds=600)
    print("After downtime slashing:", updated_stakes)
