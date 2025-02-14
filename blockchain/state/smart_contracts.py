import hashlib
import json
import time

class SmartContractEngine:
    """Handles execution, validation, and state management for smart contracts."""

    def __init__(self, initial_contracts=None):
        """
        Initializes the SmartContractEngine.
        :param initial_contracts: A dictionary of deployed smart contracts and their states.
        """
        self.contracts = initial_contracts or {}

    def deploy_contract(self, contract_code, creator, initial_state=None):
        """
        Deploys a new smart contract.
        :param contract_code: The code of the smart contract (e.g., Python code or a bytecode string).
        :param creator: The address of the contract creator.
        :param initial_state: The initial state of the contract.
        :return: The contract address (hash of the contract code and creator).
        """
        contract_address = self._compute_contract_address(contract_code, creator)
        self.contracts[contract_address] = {
            "creator": creator,
            "code": contract_code,
            "state": initial_state or {},
            "timestamp": int(time.time())
        }
        print(f"Contract deployed at address: {contract_address}")
        return contract_address

    def execute(self, transaction, state_manager):
        """
        Executes a smart contract based on the provided transaction.
        :param transaction: The transaction that triggers the smart contract.
        :param state_manager: The StateManager instance to access global state.
        """
        contract_address = transaction["receiver"]
        contract = self.contracts.get(contract_address)

        if not contract:
            raise ValueError(f"Contract at address {contract_address} not found.")

        # Simulate contract execution by running its code (in real use, use a safe VM)
        contract_code = compile(contract["code"], "<string>", "exec")
        exec_context = {
            "state": contract["state"],
            "transaction": transaction,
            "global_state": state_manager,
            "result": None
        }
        exec(contract_code, {}, exec_context)

        # Update the contract state after execution
        contract["state"] = exec_context["state"]
        print(f"Contract {contract_address} executed successfully.")

    def validate_contract(self, contract_code):
        """
        Validates the contract code to ensure it meets basic requirements.
        :param contract_code: The code of the smart contract.
        :return: True if valid, raises an error otherwise.
        """
        if not isinstance(contract_code, str) or len(contract_code) == 0:
            raise ValueError("Invalid contract code: must be a non-empty string.")
        # Additional validation can include prohibited operations, gas limits, etc.
        return True

    def get_contract_state(self, contract_address):
        """
        Retrieves the state of a deployed contract.
        :param contract_address: The address of the contract.
        :return: The state of the contract.
        """
        contract = self.contracts.get(contract_address)
        if not contract:
            raise ValueError(f"Contract at address {contract_address} not found.")
        return contract["state"]

    def rollback(self, transaction, state_manager):
        """
        Rolls back the state of a smart contract based on a failed transaction.
        :param transaction: The transaction that triggered the rollback.
        :param state_manager: The StateManager instance.
        """
        contract_address = transaction["receiver"]
        contract = self.contracts.get(contract_address)

        if not contract:
            raise ValueError(f"Contract at address {contract_address} not found.")

        # For simplicity, we assume state is backed up before every transaction
        # In production, this would be more complex and involve versioned state.
        if "backup_state" in contract:
            contract["state"] = contract["backup_state"]
            print(f"Contract {contract_address} state rolled back.")
        else:
            print(f"No backup state found for contract {contract_address}.")

    def get_state(self):
        """
        Returns the current state of all contracts.
        :return: A dictionary of all contracts and their states.
        """
        return self.contracts

    def _compute_contract_address(self, contract_code, creator):
        """
        Computes a unique address for a smart contract based on its code and creator.
        :param contract_code: The code of the contract.
        :param creator: The address of the creator.
        :return: A unique contract address (SHA-256 hash).
        """
        combined_data = f"{contract_code}{creator}".encode("utf-8")
        return hashlib.sha256(combined_data).hexdigest()


# Example usage
if __name__ == "__main__":
    # Initialize the SmartContractEngine
    engine = SmartContractEngine()

    # Example contract code (Python script in string form)
    contract_code = """
def handle_event(state, transaction):
    sender = transaction["sender"]
    amount = transaction["amount"]
    if sender not in state:
        state[sender] = 0
    state[sender] += amount
state["last_updated"] = transaction["timestamp"]
"""

    # Deploy the contract
    creator_address = "Alice"
    contract_address = engine.deploy_contract(contract_code, creator_address)

    # Simulate a transaction to trigger the contract
    transaction = {
        "sender": "Bob",
        "receiver": contract_address,
        "amount": 100,
        "timestamp": int(time.time())
    }

    # Simulate state manager (mock for this example)
    class MockStateManager:
        pass

    state_manager = MockStateManager()

    # Execute the contract
    engine.execute(transaction, state_manager)

    # Retrieve the contract state
    state = engine.get_contract_state(contract_address)
    print("Contract State:", state)
