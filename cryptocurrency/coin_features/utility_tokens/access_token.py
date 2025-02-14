import hashlib
import time
from typing import Dict, Optional


class AccessToken:
    """Manages the issuance and validation of access tokens for dApp access."""

    def __init__(self, token_expiry_seconds: int):
        """
        Initializes the AccessToken system.
        :param token_expiry_seconds: Time in seconds before a token expires.
        """
        self.token_expiry_seconds = token_expiry_seconds
        self.tokens = {}  # Stores issued tokens {token: {"user": str, "expiry": int}}

    def generate_token(self, user_id: str) -> str:
        """
        Generates a new access token for a user.
        :param user_id: The unique identifier of the user.
        :return: The generated access token.
        """
        timestamp = int(time.time())
        token_data = f"{user_id}{timestamp}"
        token = hashlib.sha256(token_data.encode()).hexdigest()

        self.tokens[token] = {"user": user_id, "expiry": timestamp + self.token_expiry_seconds}
        print(f"Generated token for user '{user_id}': {token}")
        return token

    def validate_token(self, token: str) -> bool:
        """
        Validates an access token.
        :param token: The token to validate.
        :return: True if the token is valid, False otherwise.
        """
        if token not in self.tokens:
            print("Token not found.")
            return False

        token_data = self.tokens[token]
        if time.time() > token_data["expiry"]:
            print("Token has expired.")
            return False

        print(f"Token is valid for user '{token_data['user']}'.")
        return True

    def revoke_token(self, token: str) -> bool:
        """
        Revokes an access token, making it invalid.
        :param token: The token to revoke.
        :return: True if the token was successfully revoked, False otherwise.
        """
        if token in self.tokens:
            del self.tokens[token]
            print("Token revoked successfully.")
            return True
        else:
            print("Token not found.")
            return False

    def get_user_from_token(self, token: str) -> Optional[str]:
        """
        Retrieves the user associated with a valid token.
        :param token: The token to check.
        :return: The user ID if the token is valid, None otherwise.
        """
        if self.validate_token(token):
            return self.tokens[token]["user"]
        return None


# Example usage
if __name__ == "__main__":
    # Initialize the access token system with a 5-minute expiry
    access_token_system = AccessToken(token_expiry_seconds=300)

    # Generate a token for a user
    token = access_token_system.generate_token(user_id="user123")

    # Validate the token
    print("\nValidating Token:")
    is_valid = access_token_system.validate_token(token)
    print("Token valid:", is_valid)

    # Get the user from the token
    print("\nRetrieving User from Token:")
    user = access_token_system.get_user_from_token(token)
    print("User:", user)

    # Revoke the token
    print("\nRevoking Token:")
    access_token_system.revoke_token(token)

    # Validate the token after revocation
    print("\nValidating Token After Revocation:")
    is_valid = access_token_system.validate_token(token)
    print("Token valid:", is_valid)
