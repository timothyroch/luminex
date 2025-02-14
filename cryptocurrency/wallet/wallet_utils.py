import hashlib
import base58 # type: ignore
import qrcode # type: ignore
from cryptography.hazmat.primitives.serialization import load_pem_public_key # type: ignore
from cryptography.hazmat.primitives import hashes # type: ignore


class WalletUtils:
    """Provides utility functions for wallet operations."""

    @staticmethod
    def generate_address(public_key_pem):
        """
        Generates a blockchain wallet address from a public key.
        :param public_key_pem: The public key in PEM format (string).
        :return: The generated wallet address (string).
        """
        # Load the public key
        public_key = load_pem_public_key(public_key_pem.encode('utf-8'))

        # Get the public key bytes
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Perform SHA-256 hash on the public key
        sha256_hash = hashlib.sha256(public_key_bytes).digest()

        # Perform RIPEMD-160 hash on the SHA-256 hash
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_hash)
        hashed_public_key = ripemd160.digest()

        # Add a version byte (e.g., 0x00 for Bitcoin mainnet)
        versioned_key = b'\x00' + hashed_public_key

        # Perform double SHA-256 to get the checksum
        checksum = hashlib.sha256(hashlib.sha256(versioned_key).digest()).digest()[:4]

        # Append the checksum to the versioned key
        full_key = versioned_key + checksum

        # Encode the result in Base58
        address = base58.b58encode(full_key).decode('utf-8')
        return address

    @staticmethod
    def create_qr_code(data, file_path="wallet_qr.png"):
        """
        Generates a QR code for the given data and saves it as an image file.
        :param data: The data to encode in the QR code (string).
        :param file_path: The file path to save the QR code image (default: "wallet_qr.png").
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save(file_path)
        print(f"QR code saved to {file_path}.")

    @staticmethod
    def format_transaction(sender, receiver, amount):
        """
        Formats a transaction for signing or broadcasting.
        :param sender: The sender's wallet address (string).
        :param receiver: The receiver's wallet address (string).
        :param amount: The amount to transfer (float).
        :return: A formatted transaction dictionary.
        """
        return {
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        }


# Example usage
if __name__ == "__main__":
    # Example public key (replace with actual generated key)
    public_key_pem = """-----BEGIN PUBLIC KEY-----
    ...
    -----END PUBLIC KEY-----"""

    # Generate wallet address
    wallet_utils = WalletUtils()
    address = wallet_utils.generate_address(public_key_pem)
    print("Generated Address:", address)

    # Create a QR code for the address
    wallet_utils.create_qr_code(address, file_path="my_wallet_qr.png")

    # Format a transaction
    transaction = wallet_utils.format_transaction(
        sender=address,
        receiver="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        amount=50.0
    )
    print("Formatted Transaction:", transaction)
