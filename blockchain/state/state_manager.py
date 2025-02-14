import json
from blockchain.state.utxo_set import UTXOSet
from blockchain.state.smart_contracts import SmartContractEngine

class StateManager:
    """Manages the global state of the blockchain, including balances, UTXOs, and smart contracts."""

    def __init__(self, initial_state_path="blockchain/state/initial_state.json"):
        """
        Initializes the StateManager.
        :param initial_state_path: Path to the initial state file (used for genesis block or recovery).
        """
        with open(initial_state_path, "r") as file:
            self.state = json.load(file)

        self.utxo_set = UTXOSet(self.state["utxo_set"])
        self.smart_contract_engine = SmartContractEngine(self.state["smart_contracts"])
        self.balances = self.state["balances"]
        self.nonces = self.state["nonces"]

    def update_state(self, block):
        """
        Updates the global state based on the transactions in the block.
        :param block: The block containing the transactions to process.
        :return: True if the state is updated successfully, False otherwise.
        """
        try:
            for transaction in block.transactions:
                self._process_transaction(transaction)
            self._update_utxo_set(block)
            return True
        except Exception as e:
            print(f"Failed to update state: {e}")
            return False

    def _process_transaction(self, transaction):
        """
        Processes a single transaction, updating balances and nonces.
        :param transaction: The transaction to process.
        """
        sender = transaction["sender"]
        receiver = transaction["receiver"]
        amount = transaction["amount"]
        fee = transaction.get("fee", 0)

        # Deduct amount and fee from sender
        self.balances[sender] -= (amount + fee)
        self.nonces[sender] += 1

        # Add amount to receiver
        if receiver not in self.balances:
            self.balances[receiver] = 0
        self.balances[receiver] += amount

        # Smart contract execution if receiver is a contract
        if "contract_code" in transaction:
            self.smart_contract_engine.execute(transaction, self)

    def _update_utxo_set(self, block):
        """
        Updates the UTXO set based on the transactions in the block.
        :param block: The block containing the transactions to process.
        """
        for transaction in block.transactions:
            self.utxo_set.apply_transaction(transaction)

    def get_balance(self, account):
        """
        Retrieves the balance of a given account.
        :param account: The account to query.
        :return: The balance of the account.
        """
        return self.balances.get(account, 0)

    def get_nonce(self, account):
        """
        Retrieves the nonce of a given account.
        :param account: The account to query.
        :return: The nonce of the account.
        """
        return self.nonces.get(account, 0)

    def save_state(self, file_path="blockchain/state/current_state.json"):
        """
        Saves the current state to a file for persistence.
        :param file_path: Path to the file where the state will be saved.
        """
        current_state = {
            "balances": self.balances,
            "nonces": self.nonces,
            "utxo_set": self.utxo_set.get_state(),
            "smart_contracts": self.smart_contract_engine.get_state()
        }

        with open(file_path, "w") as file:
            json.dump(current_state, file, indent=4)

    def rollback_state(self, block):
        """
        Rolls back the state to undo the changes from a given block.
        :param block: The block whose transactions should be undone.
        """
        try:
            for transaction in reversed(block.transactions):
                self._rollback_transaction(transaction)
            self.utxo_set.rollback_block(block)
        except Exception as e:
            print(f"Failed to rollback state: {e}")

    def _rollback_transaction(self, transaction):
        """
        Rolls back a single transaction.
        :param transaction: The transaction to rollback.
        """
        sender = transaction["sender"]
        receiver = transaction["receiver"]
        amount = transaction["amount"]
        fee = transaction.get("fee", 0)

        # Revert balances and nonces
        self.balances[sender] += (amount + fee)
        self.nonces[sender] -= 1
        self.balances[receiver] -= amount

        # Rollback smart contract if applicable
        if "contract_code" in transaction:
            self.smart_contract_engine.rollback(transaction, self)


# Example usage
if __name__ == "__main__":
    from blockchain.blocks.block import Block

    # Example initial state
    initial_state = {
        "balances": {"Alice": 100, "Bob": 50},
        "nonces": {"Alice": 1, "Bob": 0},
        "utxo_set": [],
        "smart_contracts": {}
    }

    # Save initial state to file
    with open("blockchain/state/initial_state.json", "w") as file:
        json.dump(initial_state, file, indent=4)

    # Load state manager
    state_manager = StateManager()

    # Example block with transactions
    block = Block(
        index=1,
        previous_hash="0" * 64,
        timestamp=1678912345,
        transactions=[
            {"sender": "Alice", "receiver": "Bob", "amount": 20, "fee": 1, "nonce": 2},
            {"sender": "Bob", "receiver": "Alice", "amount": 10, "fee": 0.5, "nonce": 1}
        ],
        nonce=0,
        block_hash=""
    )

    # Update state with the block
    if state_manager.update_state(block):
        print("State updated successfully.")
        print("Alice's balance:", state_manager.get_balance("Alice"))
        print("Bob's balance:", state_manager.get_balance("Bob"))

    # Save the current state
    state_manager.save_state()
