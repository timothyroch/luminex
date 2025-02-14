import hashlib
import hmac
import base64
from typing import Dict, Any
from cryptography.hazmat.primitives import hashes # type: ignore
from cryptography.hazmat.primitives.asymmetric import ec # type: ignore
from cryptography.hazmat.primitives.kdf.hkdf import HKDF # type: ignore
from cryptography.hazmat.primitives.serialization import ( # type: ignore
    Encoding,
    PrivateFormat,
    PublicFormat,
    NoEncryption,
    load_pem_private_key,
    load_pem_public_key,
)


class OffchainSigning:
    """Handles signing and verification of off-chain transactions."""

    def __init__(self):
        pass

    @staticmethod
    def generate_key_pair() -> Dict[str, str]:
        """
        Generates a new ECDSA key pair for signing and verification.
        :return: A dictionary containing the private and public keys in PEM format.
        """
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()

        private_key_pem = private_key.private_bytes(
            Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()
        )
        public_key_pem = public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

        return {
            "private_key": private_key_pem.decode(),
            "public_key": public_key_pem.decode(),
        }

    @staticmethod
    def sign_transaction(private_key_pem: str, transaction_data: Dict[str, Any]) -> str:
        """
        Signs a transaction using the provided private key.
        :param private_key_pem: The private key in PEM format.
        :param transaction_data: The transaction data to sign.
        :return: The transaction signature as a base64-encoded string.
        """
        private_key = load_pem_private_key(private_key_pem.encode(), password=None)
        transaction_bytes = OffchainSigning._serialize_transaction(transaction_data)
        signature = private_key.sign(transaction_bytes, ec.ECDSA(hashes.SHA256()))
        return base64.b64encode(signature).decode()

    @staticmethod
    def verify_signature(public_key_pem: str, transaction_data: Dict[str, Any], signature: str) -> bool:
        """
        Verifies a transaction signature using the provided public key.
        :param public_key_pem: The public key in PEM format.
        :param transaction_data: The transaction data to verify.
        :param signature: The transaction signature (base64-encoded).
        :return: True if the signature is valid, False otherwise.
        """
        public_key = load_pem_public_key(public_key_pem.encode())
        transaction_bytes = OffchainSigning._serialize_transaction(transaction_data)
        signature_bytes = base64.b64decode(signature)

        try:
            public_key.verify(signature_bytes, transaction_bytes, ec.ECDSA(hashes.SHA256()))
            return True
        except Exception as e:
            print(f"Signature verification failed: {e}")
            return False

    @staticmethod
    def _serialize_transaction(transaction_data: Dict[str, Any]) -> bytes:
        """
        Serializes transaction data into a deterministic byte format.
        :param transaction_data: The transaction data to serialize.
        :return: Serialized transaction as bytes.
        """
        return str(sorted(transaction_data.items())).encode()


# Example usage
if __name__ == "__main__":
    signing = OffchainSigning()

    # Generate a new key pair
    keys = signing.generate_key_pair()
    print("Private Key:\n", keys["private_key"])
    print("Public Key:\n", keys["public_key"])

    # Transaction data
    transaction = {
        "sender": "address1",
        "receiver": "address2",
        "amount": 100.0,
        "timestamp": 1673445600,
    }

    # Sign the transaction
    signature = signing.sign_transaction(keys["private_key"], transaction)
    print("\nSignature:", signature)

    # Verify the signature
    is_valid = signing.verify_signature(keys["public_key"], transaction, signature)
    print("\nSignature valid?", is_valid)
