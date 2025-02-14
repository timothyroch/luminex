import hashlib
import hmac
import json
from typing import Dict


def generate_transaction_id(sender: str, receiver: str, amount: float, timestamp: float) -> str:
    """
    Generates a unique transaction ID using a hash of the transaction details.
    :param sender: Sender's address.
    :param receiver: Receiver's address.
    :param amount: Transaction amount.
    :param timestamp: Transaction timestamp.
    :return: Unique transaction ID.
    """
    transaction_string = f"{sender}{receiver}{amount}{timestamp}"
    return hashlib.sha256(transaction_string.encode()).hexdigest()


def sign_transaction(private_key: str, transaction: Dict[str, any]) -> str:
    """
    Signs a transaction using HMAC with the provided private key.
    :param private_key: The sender's private key.
    :param transaction: The transaction data.
    :return: The transaction signature.
    """
    transaction_data = json.dumps(
        {key: transaction[key] for key in transaction if key != "signature"},
        sort_keys=True
    ).encode()
    return hmac.new(private_key.encode(), transaction_data, hashlib.sha256).hexdigest()


def verify_signature(public_key: str, transaction: Dict[str, any], signature: str) -> bool:
    """
    Verifies the signature of a transaction.
    :param public_key: The sender's public key.
    :param transaction: The transaction data.
    :param signature: The provided transaction signature.
    :return: True if the signature is valid, False otherwise.
    """
    transaction_data = json.dumps(
        {key: transaction[key] for key in transaction if key != "signature"},
        sort_keys=True
    ).encode()

    # Simulate public key-based HMAC validation (replace with actual ECDSA verification in production)
    expected_signature = hmac.new(public_key.encode(), transaction_data, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_signature, signature)


def calculate_transaction_fee(base_fee: float, amount: float) -> float:
    """
    Calculates the transaction fee based on the base fee and transaction amount.
    :param base_fee: The base fee for the transaction.
    :param amount: The transaction amount.
    :return: The calculated transaction fee.
    """
    return base_fee + (0.01 * amount)  # Example: 1% of the transaction amount as a fee


def serialize_transaction(transaction: Dict[str, any]) -> str:
    """
    Serializes a transaction into a JSON string.
    :param transaction: The transaction data.
    :return: Serialized JSON string.
    """
    return json.dumps(transaction, sort_keys=True)


def deserialize_transaction(transaction_str: str) -> Dict[str, any]:
    """
    Deserializes a JSON string back into a transaction dictionary.
    :param transaction_str: The serialized transaction string.
    :return: Deserialized transaction dictionary.
    """
    return json.loads(transaction_str)
