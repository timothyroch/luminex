import os
from cryptography.hazmat.primitives.asymmetric import ec # type: ignore
from cryptography.hazmat.primitives.kdf.hkdf import HKDF # type: ignore
from cryptography.hazmat.primitives import hashes # type: ignore
from cryptography.hazmat.primitives.kdf.kbkdf import ConcatKDFHash # type: ignore
from cryptography.hazmat.primitives.serialization import ( # type: ignore
    load_pem_public_key,
    load_pem_private_key,
    Encoding,
    PublicFormat,
    PrivateFormat,
    NoEncryption,
)
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed # type: ignore
from cryptography.hazmat.primitives.hashes import SHA256 # type: ignore
from cryptography.exceptions import InvalidSignature # type: ignore

class KeyExchange:
    """Handles secure key exchange using Elliptic Curve Diffie-Hellman (ECDH)."""

    def __init__(self):
        """Initializes KeyExchange with a new ECDH private key."""
        self.private_key = ec.generate_private_key(ec.SECP256R1())
        self.public_key = self.private_key.public_key()

    def get_public_key(self):
        """Returns the public key in PEM format."""
        return self.public_key.public_bytes(
            Encoding.PEM, PublicFormat.SubjectPublicKeyInfo
        )

    def generate_shared_secret(self, peer_public_key_pem):
        """
        Derives a shared secret using the peer's public key.
        :param peer_public_key_pem: The peer's public key in PEM format.
        :return: A derived session key.
        """
        peer_public_key = load_pem_public_key(peer_public_key_pem)
        shared_secret = self.private_key.exchange(ec.ECDH(), peer_public_key)

        # Derive a symmetric session key using HKDF
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"key-exchange",
        ).derive(shared_secret)

        return derived_key

    def sign_message(self, message):
        """
        Signs a message with the private key.
        :param message: The message to sign.
        :return: The signature.
        """
        return self.private_key.sign(
            message, ec.ECDSA(Prehashed(SHA256()))
        )

    def verify_signature(self, peer_public_key_pem, message, signature):
        """
        Verifies the signature of a message using the peer's public key.
        :param peer_public_key_pem: The peer's public key in PEM format.
        :param message: The message to verify.
        :param signature: The signature to verify.
        :return: True if valid, raises InvalidSignature otherwise.
        """
        peer_public_key = load_pem_public_key(peer_public_key_pem)
        try:
            peer_public_key.verify(signature, message, ec.ECDSA(Prehashed(SHA256())))
            return True
        except InvalidSignature:
            raise InvalidSignature("Signature verification failed.")

    def save_private_key(self, file_path):
        """Saves the private key to a file."""
        with open(file_path, "wb") as file:
            file.write(
                self.private_key.private_bytes(
                    Encoding.PEM,
                    PrivateFormat.PKCS8,
                    NoEncryption(),
                )
            )

    def load_private_key(self, file_path):
        """Loads the private key from a file."""
        with open(file_path, "rb") as file:
            self.private_key = load_pem_private_key(file.read(), password=None)
            self.public_key = self.private_key.public_key()

# Example usage
if __name__ == "__main__":
    # Node A generates key pair
    node_a = KeyExchange()
    public_key_a = node_a.get_public_key()

    # Node B generates key pair
    node_b = KeyExchange()
    public_key_b = node_b.get_public_key()

    # Exchange public keys and generate shared secrets
    shared_secret_a = node_a.generate_shared_secret(public_key_b)
    shared_secret_b = node_b.generate_shared_secret(public_key_a)

    # Ensure shared secrets are identical
    assert shared_secret_a == shared_secret_b, "Shared secrets do not match!"
    print("Shared secret established successfully!")

    # Node A signs a message
    message = b"Blockchain transaction"
    signature = node_a.sign_message(message)

    # Node B verifies the signature
    try:
        valid = node_b.verify_signature(public_key_a, message, signature)
        print("Signature is valid!") if valid else print("Signature is invalid!")
    except InvalidSignature as e:
        print(e)
