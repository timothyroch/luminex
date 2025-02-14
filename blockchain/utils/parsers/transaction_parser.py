import json
from hashlib import sha256
from cryptography.hazmat.primitives import hashes # type: ignore
from cryptography.hazmat.primitives.asymmetric import ec # type: ignore
from cryptography.hazmat.primitives.serialization import load_pem_public_key # type: ignore
from cryptography.exceptions import InvalidSignature # type: ignore


class TransactionParser:
    """Parses and validates raw transaction data."""

    @staticmethod
    def parse_raw_transaction(raw_transaction):
        """
        Parses raw transaction data into a structured dictionary.
        :param raw_transaction: The raw transaction data (JSON or binary format).
        :return: A structured transaction dictionary.
        """
        try:
            if isinstance(raw_transaction, bytes):
                transaction_data = json.loads(raw_transaction.decode('utf-8'))
            elif isinstance(raw_transaction, str):
                transaction_data = json.loads(raw_transaction)
            else:
                raise ValueError("Unsupported transaction data format.")
            return transaction_data
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Failed to parse transaction: {e}")

    @staticmethod
    def validate_transaction_structure(transaction):
        """
        Validates the structure of a transaction.
        :param transaction: The transaction data as a dictionary.
        :return: True if the structure is valid, raises ValueError otherwise.
        """
        required_fields = ["sender", "receiver", "amount", "signature", "public_key"]
        for field in required_fields:
            if field not in transaction:
                raise ValueError(f"Missing required transaction field: {field}")
        if not isinstance(transaction["amount"], (int, float)) or transaction["amount"] <= 0:
            raise ValueError("Transaction amount must be a positive number.")
        return True

    @staticmethod
    def verify_signature(transaction):
        """
        Verifies the digital signature of a transaction.
        :param transaction: The transaction data as a dictionary.
        :return: True if the signature is valid, raises ValueError otherwise.
        """
        try:
            # Extract fields for signature verification
            public_key_pem = transaction["public_key"]
            signature = bytes.fromhex(transaction["signature"])
            message = f"{transaction['sender']}{transaction['receiver']}{transaction['amount']}".encode('utf-8')

            # Load the public key
            public_key = load_pem_public_key(public_key_pem.encode('utf-8'))

            # Verify the signature
            public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            raise ValueError("Invalid digital signature.")
        except Exception as e:
            raise ValueError(f"Failed to verify signature: {e}")

    @staticmethod
    def validate_transaction(transaction):
        """
        Fully validates a transaction by checking its structure and signature.
        :param transaction: The transaction data as a dictionary.
        :return: True if the transaction is valid, raises ValueError otherwise.
        """
        TransactionParser.validate_transaction_structure(transaction)
        TransactionParser.verify_signature(transaction)
        return True


# Example usage
if __name__ == "__main__":
    # Example raw transaction (in JSON format)
    raw_transaction = """
    {
        "sender": "Alice",
        "receiver": "Bob",
        "amount": 50,
        "signature": "d1c3d8ec5f4f3e5d6b8b9c17de8e53936a63af7f5b4c0e7b7b6c8f2edc5a6d7c",
        "public_key": "-----BEGIN PUBLIC KEY-----\\n...\\n-----END PUBLIC KEY-----"
    }
    """

    try:
        parser = TransactionParser()
        transaction = parser.parse_raw_transaction(raw_transaction)
        print("Parsed Transaction:", transaction)

        # Validate transaction
        if parser.validate_transaction(transaction):
            print("Transaction is valid.")
    except ValueError as e:
        print("Transaction validation failed:", e)
