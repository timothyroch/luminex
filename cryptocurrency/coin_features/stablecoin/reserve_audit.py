import json
import time
from typing import Dict, List, Union


class ReserveAudit:
    """Audits reserves backing a stablecoin to ensure transparency and stability."""

    def __init__(self, reserve_file: str):
        """
        Initializes the ReserveAudit system.
        :param reserve_file: Path to the reserve data file.
        """
        self.reserve_file = reserve_file

    def load_reserve_data(self) -> Dict:
        """
        Loads the reserve data from a JSON file.
        :return: A dictionary of reserve data.
        """
        with open(self.reserve_file, "r") as file:
            return json.load(file)

    def save_reserve_data(self, data: Dict):
        """
        Saves updated reserve data to the JSON file.
        :param data: Updated reserve data.
        """
        with open(self.reserve_file, "w") as file:
            json.dump(data, file, indent=4)

    def perform_audit(self) -> Dict[str, Union[bool, str, float]]:
        """
        Performs an audit of the reserves.
        :return: Audit results, including the reserve status and total backing.
        """
        reserve_data = self.load_reserve_data()
        total_reserves = sum(asset["value"] for asset in reserve_data["assets"])
        total_liabilities = reserve_data["total_liabilities"]

        if total_reserves >= total_liabilities:
            return {
                "status": "pass",
                "message": "Reserves are sufficient to cover liabilities.",
                "total_reserves": total_reserves,
                "total_liabilities": total_liabilities
            }
        else:
            return {
                "status": "fail",
                "message": "Reserves are insufficient to cover liabilities.",
                "total_reserves": total_reserves,
                "total_liabilities": total_liabilities
            }

    def add_reserve_asset(self, name: str, value: float):
        """
        Adds a new reserve asset.
        :param name: Name of the asset.
        :param value: Value of the asset.
        """
        reserve_data = self.load_reserve_data()
        reserve_data["assets"].append({"name": name, "value": value})
        self.save_reserve_data(reserve_data)
        print(f"Added reserve asset '{name}' with value {value}.")

    def remove_reserve_asset(self, name: str):
        """
        Removes a reserve asset by name.
        :param name: Name of the asset to remove.
        """
        reserve_data = self.load_reserve_data()
        reserve_data["assets"] = [asset for asset in reserve_data["assets"] if asset["name"] != name]
        self.save_reserve_data(reserve_data)
        print(f"Removed reserve asset '{name}'.")

    def list_reserve_assets(self) -> List[Dict]:
        """
        Lists all current reserve assets.
        :return: A list of reserve assets.
        """
        reserve_data = self.load_reserve_data()
        return reserve_data["assets"]


# Example usage
if __name__ == "__main__":
    # Initialize ReserveAudit with example reserve data file
    audit = ReserveAudit(reserve_file="reserves.json")

    # Perform an audit
    result = audit.perform_audit()
    print("\nAudit Results:", result)

    # Add a new reserve asset
    audit.add_reserve_asset(name="Gold", value=500000)

    # Remove an existing reserve asset
    audit.remove_reserve_asset(name="USD Deposits")

    # List current reserve assets
    print("\nCurrent Reserve Assets:", audit.list_reserve_assets())
