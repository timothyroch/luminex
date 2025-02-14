from cryptography.hazmat.primitives import hashes # type: ignore
from cryptography.hazmat.primitives.asymmetric import ec # type: ignore
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key # type: ignore
from cryptography.exceptions import InvalidSignature # type: ignore


class KeySigner:
    """Handles signing and verifying blockchain transactions."""

    @staticmethod
    def sign_message(message, private_key_pem):
        """
        Signs a message using the provided private key.
        :param message: The message to sign (string).
        :param private_key_pem: The private key in PEM format.
        :return: The signature as a hexadecimal string.
        """
        # Load the private key
        private_key = load_pem_private_key(private_key_pem.encode('utf-8'), password=None)

        # Sign the message
        signature = private_key.sign(
            message.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        return signature.hex()

    @staticmethod
    def verify_signature(message, signature, public_key_pem):
        """
        Verifies a signature using the provided public key.
        :param message: The original message (string).
        :param signature: The signature to verify (hexadecimal string).
        :param public_key_pem: The public key in PEM format.
        :return: True if the signature is valid, raises ValueError otherwise.
        """
        try:
            # Load the public key
            public_key = load_pem_public_key(public_key_pem.encode('utf-8'))

            # Verify the signature
            public_key.verify(
                bytes.fromhex(signature),
                message.encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            raise ValueError("Invalid signature.")
        except Exception as e:
            raise ValueError(f"Failed to verify signature: {e}")


# Example usage
if __name__ == "__main__":
    # Sample private and public keys (for testing purposes; use generated keys in production)
    private_key_pem = """-----BEGIN PRIVATE KEY-----
    ...
    -----END PRIVATE KEY-----"""
    public_key_pem = """-----BEGIN PUBLIC KEY-----
    ...
    -----END PUBLIC KEY-----"""

    # Message to be signed
    message = "Alice sends 50 coins to Bob"

    try:
        # Sign the message
        signer = KeySigner()
        signature = signer.sign_message(message, private_key_pem)
        print("Signature:", signature)

        # Verify the signature
        is_valid = signer.verify_signature(message, signature, public_key_pem)
        print("Signature is valid:", is_valid)

    except ValueError as e:
        print("Error:", e)
