from cryptography.hazmat.primitives.asymmetric import ec # type: ignore
from cryptography.hazmat.primitives import hashes # type: ignore
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature # type: ignore
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC # type: ignore
from cryptography.hazmat.primitives import serialization # type: ignore
from cryptography.hazmat.backends import default_backend # type: ignore
import os
import base64

class DigitalSignature:
    """Provides tools for generating keys, signing data, and verifying signatures."""

    def generate_key_pair(self):
        """
        Generates a new ECDSA key pair.
        :return: A tuple (private_key, public_key) where keys are in PEM format.
        """
        private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        public_key = private_key.public_key()

        # Serialize keys to PEM format
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return private_pem.decode("utf-8"), public_pem.decode("utf-8")

    def sign_data(self, private_key_pem, data):
        """
        Signs the given data using the provided private key.
        :param private_key_pem: The private key in PEM format.
        :param data: The data to sign (string or bytes).
        :return: The signature as a base64-encoded string.
        """
        if isinstance(data, str):
            data = data.encode('utf-8')

        private_key = serialization.load_pem_private_key(
            private_key_pem.encode("utf-8"), password=None, backend=default_backend()
        )

        signature = private_key.sign(
            data,
            ec.ECDSA(hashes.SHA256())
        )

        # Encode the signature in base64 for easy transport
        return base64.b64encode(signature).decode("utf-8")

    def verify_signature(self, public_key_pem, data, signature):
        """
        Verifies a signature against the provided data and public key.
        :param public_key_pem: The public key in PEM format.
        :param data: The data to verify (string or bytes).
        :param signature: The base64-encoded signature to verify.
        :return: True if the signature is valid, False otherwise.
        """
        if isinstance(data, str):
            data = data.encode('utf-8')

        public_key = serialization.load_pem_public_key(
            public_key_pem.encode("utf-8"), backend=default_backend()
        )

        signature_bytes = base64.b64decode(signature)

        try:
            public_key.verify(
                signature_bytes,
                data,
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except Exception as e:
            print(f"Signature verification failed: {e}")
            return False


# Example usage
if __name__ == "__main__":
    ds = DigitalSignature()

    # Generate a new key pair
    private_key, public_key = ds.generate_key_pair()
    print("Private Key:\n", private_key)
    print("Public Key:\n", public_key)

    # Sign some data
    data = "This is a test message for blockchain!"
    signature = ds.sign_data(private_key, data)
    print("Signature:", signature)

    # Verify the signature
    is_valid = ds.verify_signature(public_key, data, signature)
    print("Signature Valid:", is_valid)

    # Verify with modified data (should fail)
    modified_data = "This is a tampered message!"
    is_valid = ds.verify_signature(public_key, modified_data, signature)
    print("Signature Valid on Modified Data:", is_valid)
