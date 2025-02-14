import hashlib
import json
from typing import Optional
from cryptography.hazmat.primitives.asymmetric import rsa, padding # type: ignore
from cryptography.hazmat.primitives import hashes, serialization # type: ignore


class Transaction:
    def __init__(self, sender: str, receiver: str, amount: float, signature: Optional[str] = None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = self.get_timestamp()
        self.signature = signature

    def get_timestamp(self) -> int:
        """Returns the current timestamp."""
        import time
        return int(time.time())

    def calculate_hash(self) -> str:
        """Calculates the hash of the transaction."""
        tx_content = f"{self.sender}{self.receiver}{self.amount}{self.timestamp}"
        return hashlib.sha256(tx_content.encode()).hexdigest()

    def sign_transaction(self, private_key: rsa.RSAPrivateKey):
        """Signs the transaction using the sender's private key."""
        tx_hash = self.calculate_hash()
        self.signature = private_key.sign(
            tx_hash.encode(),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        ).hex()

    def verify_signature(self, public_key: rsa.RSAPublicKey) -> bool:
        """Verifies the transaction's signature using the sender's public key."""
        try:
            tx_hash = self.calculate_hash()
            public_key.verify(
                bytes.fromhex(self.signature),
                tx_hash.encode(),
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            print(f"Signature verification failed: {e}")
            return False

    def to_dict(self) -> dict:
        """Serializes the transaction to a dictionary."""
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "signature": self.signature
        }

    @staticmethod
    def from_dict(data: dict) -> 'Transaction':
        """Deserializes a dictionary into a Transaction object."""
        return Transaction(
            sender=data["sender"],
            receiver=data["receiver"],
            amount=data["amount"],
            signature=data.get("signature")
        )

    def is_valid(self, sender_balance: float) -> bool:
        """Validates the transaction."""
        if sender_balance < self.amount:
            print("Insufficient balance.")
            return False
        if not self.signature:
            print("Transaction is unsigned.")
            return False
        return True


# Example usage
if __name__ == "__main__":
    # Generate RSA keys for demonstration
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    tx = Transaction("Alice", "Bob", 50.0)
    tx.sign_transaction(private_key)
    print("Transaction is valid:", tx.verify_signature(public_key))
    print(tx.to_dict())
