from cryptography.hazmat.primitives import hashes # type: ignore
from cryptography.hazmat.primitives.asymmetric import ec # type: ignore
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key # type: ignore
from cryptography.exceptions import InvalidSignature # type: ignore


class MultiSigWallet:
    """Implements multi-signature wallet functionality."""

    def __init__(self, required_signatures, public_keys):
        """
        Initializes the multisig wallet.
        :param required_signatures: Number of signatures required to authorize a transaction.
        :param public_keys: List of public keys for the wallet participants.
        """
        if required_signatures > len(public_keys):
            raise ValueError("Required signatures cannot exceed the number of public keys.")
        self.required_signatures = required_signatures
        self.public_keys = [load_pem_public_key(pk.encode('utf-8')) for pk in public_keys]

    def verify_transaction(self, message, signatures):
        """
        Verifies that the transaction has the required number of valid signatures.
        :param message: The message to verify (string).
        :param signatures: List of (public_key, signature) tuples.
        :return: True if the required number of valid signatures is met, False otherwise.
        """
        valid_signatures = 0

        for pub_key_pem, signature in signatures:
            try:
                public_key = load_pem_public_key(pub_key_pem.encode('utf-8'))
                public_key.verify(
                    bytes.fromhex(signature),
                    message.encode('utf-8'),
                    ec.ECDSA(hashes.SHA256())
                )
                if public_key in self.public_keys:
                    valid_signatures += 1
            except InvalidSignature:
                continue
            except Exception as e:
                raise ValueError(f"Error verifying signature: {e}")

        return valid_signatures >= self.required_signatures

    @staticmethod
    def sign_message(message, private_key_pem):
        """
        Signs a message using a private key.
        :param message: The message to sign (string).
        :param private_key_pem: The private key in PEM format.
        :return: The signature as a hexadecimal string.
        """
        private_key = load_pem_private_key(private_key_pem.encode('utf-8'), password=None)
        signature = private_key.sign(
            message.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        return signature.hex()


# Example usage
if __name__ == "__main__":
    # Example keys (replace with actual generated keys)
    private_keys = [
        """-----BEGIN PRIVATE KEY-----
        ...
        -----END PRIVATE KEY-----""",
        """-----BEGIN PRIVATE KEY-----
        ...
        -----END PRIVATE KEY-----"""
    ]

    public_keys = [
        """-----BEGIN PUBLIC KEY-----
        ...
        -----END PUBLIC KEY-----""",
        """-----BEGIN PUBLIC KEY-----
        ...
        -----END PUBLIC KEY-----"""
    ]

    # Initialize a multisig wallet with 2-of-2 signature requirement
    multisig_wallet = MultiSigWallet(required_signatures=2, public_keys=public_keys)

    # Message to sign
    message = "Transaction: Alice sends 100 coins to Bob"

    # Sign the message with each private key
    signatures = [
        (public_keys[0], MultiSigWallet.sign_message(message, private_keys[0])),
        (public_keys[1], MultiSigWallet.sign_message(message, private_keys[1]))
    ]

    # Verify the transaction
    is_valid = multisig_wallet.verify_transaction(message, signatures)
    print("Transaction is valid:", is_valid)
