from cryptography.hazmat.primitives.asymmetric import ec # type: ignore
from cryptography.hazmat.primitives import serialization # type: ignore
from cryptography.hazmat.backends import default_backend # type: ignore


class KeyGenerator:
    """Generates public/private key pairs for blockchain wallets."""

    def __init__(self, curve=ec.SECP256R1()):
        """
        Initializes the KeyGenerator with a specified elliptic curve.
        :param curve: The elliptic curve to use (default: SECP256R1).
        """
        self.curve = curve

    def generate_key_pair(self):
        """
        Generates a public/private key pair.
        :return: A tuple (private_key, public_key) in PEM format.
        """
        # Generate private key
        private_key = ec.generate_private_key(self.curve, default_backend())
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

        return private_pem.decode('utf-8'), public_pem.decode('utf-8')

    def save_keys_to_files(self, private_key, public_key, private_key_file="private_key.pem", public_key_file="public_key.pem"):
        """
        Saves the private and public keys to files.
        :param private_key: The private key in PEM format.
        :param public_key: The public key in PEM format.
        :param private_key_file: File to save the private key (default: "private_key.pem").
        :param public_key_file: File to save the public key (default: "public_key.pem").
        """
        with open(private_key_file, 'w') as priv_file:
            priv_file.write(private_key)
        with open(public_key_file, 'w') as pub_file:
            pub_file.write(public_key)
        print(f"Private key saved to {private_key_file}")
        print(f"Public key saved to {public_key_file}")


# Example usage
if __name__ == "__main__":
    key_gen = KeyGenerator()

    # Generate key pair
    private_key, public_key = key_gen.generate_key_pair()
    print("Generated Private Key:\n", private_key)
    print("Generated Public Key:\n", public_key)

    # Save keys to files
    key_gen.save_keys_to_files(private_key, public_key)
