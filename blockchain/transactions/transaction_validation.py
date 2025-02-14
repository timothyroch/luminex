import hashlib
import json
from cryptography.hazmat.primitives.asymmetric import rsa, padding # type: ignore
from cryptography.hazmat.primitives import hashes # type: ignore
from cryptography.hazmat.primitives.serialization import load_pem_public_key # type: ignore

class TransactionValidation:
    """Validates transactions for signature authenticity, balance sufficiency, and protocol compliance."""

    def __init__(self, blockchain_state):
        """
        Initializes the TransactionValidation with the blockchain state.
        :param blockchain_state: The current state of the blockchain for balance and nonce checks.
        """
        self.blockchain_state = blockchain_state

    @staticmethod
    def compute_transaction_hash(transaction):
        """
        Computes the hash of a transaction.
        :param transaction: The transaction dictionary.
        :return: The SHA-256 hash of the transaction as a hexadecimal string.
        """
        transaction_data = json.dumps(transaction, sort_keys=True)
        return hashlib.sha256(transaction_data.encode('utf-8')).hexdigest()

    def validate_signature(self, transaction):
        """
        Validates the digital signature of a transaction.
        :param transaction: The transaction dictionary containing the 'signature' and 'sender_public_key'.
        :return: True if the signature is valid, False otherwise.
        """
        try:
            public_key = load_pem_public_key(transaction['sender_public_key'].encode('utf-8'))
            signature = bytes.fromhex(transaction['signature'])
            transaction_copy = transaction.copy()
            del transaction_copy['signature']
            del transaction_copy['sender_public_key']
            transaction_hash = self.compute_transaction_hash(transaction_copy)

            public_key.verify(
                signature,
                transaction_hash.encode('utf-8'),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            print(f"Signature validation failed: {e}")
            return False

    def validate_balance(self, transaction):
        """
        Validates that the sender has enough balance for the transaction.
        :param transaction: The transaction dictionary.
        :return: True if the balance is sufficient, False otherwise.
        """
        sender = transaction['sender']
        amount = transaction['amount']
        fee = transaction.get('fee', 0)

        sender_balance = self.blockchain_state.get_balance(sender)
        if sender_balance >= (amount + fee):
            return True
        else:
            print(f"Insufficient balance for sender: {sender}")
            return False

    def validate_nonce(self, transaction):
        """
        Validates the nonce to prevent replay attacks.
        :param transaction: The transaction dictionary.
        :return: True if the nonce is valid, False otherwise.
        """
        sender = transaction['sender']
        transaction_nonce = transaction['nonce']

        current_nonce = self.blockchain_state.get_nonce(sender)
        if transaction_nonce == current_nonce + 1:
            return True
        else:
            print(f"Invalid nonce for sender: {sender}. Expected: {current_nonce + 1}, got: {transaction_nonce}")
            return False

    def validate_transaction(self, transaction):
        """
        Performs all validation checks on a transaction.
        :param transaction: The transaction dictionary.
        :return: True if the transaction is valid, False otherwise.
        """
        if not self.validate_signature(transaction):
            return False
        if not self.validate_balance(transaction):
            return False
        if not self.validate_nonce(transaction):
            return False
        return True


# Example usage
if __name__ == "__main__":
    # Simulated blockchain state for testing
    class MockBlockchainState:
        def __init__(self):
            self.balances = {"Alice": 100, "Bob": 50}
            self.nonces = {"Alice": 1, "Bob": 0}

        def get_balance(self, user):
            return self.balances.get(user, 0)

        def get_nonce(self, user):
            return self.nonces.get(user, 0)

    # Simulated transaction
    transaction = {
        "sender": "Alice",
        "receiver": "Bob",
        "amount": 20,
        "fee": 1,
        "nonce": 2,
        "sender_public_key": """-----BEGIN PUBLIC KEY-----
YOUR_PUBLIC_KEY_HERE
-----END PUBLIC KEY-----""",
        "signature": "YOUR_SIGNATURE_HERE"
    }

    blockchain_state = MockBlockchainState()
    validator = TransactionValidation(blockchain_state)

    # Validate transaction
    is_valid = validator.validate_transaction(transaction)
    print("Transaction is valid:", is_valid)
