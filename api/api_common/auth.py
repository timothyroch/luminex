import hashlib
import hmac
import time
from typing import Optional, Dict, Any
from flask import request, jsonify # type: ignore

# Simulated database of API keys and roles (for demonstration purposes)
API_KEYS = {
    "key1": {"role": "superadmin", "secret": "secret1"},
    "key2": {"role": "admin", "secret": "secret2"},
    "key3": {"role": "viewer", "secret": "secret3"}
}

# Token expiration time in seconds
TOKEN_EXPIRATION = 3600  # 1 hour


def generate_auth_token(api_key: str, secret: str) -> str:
    """
    Generates a time-limited authentication token using HMAC.
    :param api_key: The API key of the user.
    :param secret: The secret associated with the API key.
    :return: An authentication token.
    """
    timestamp = int(time.time())
    message = f"{api_key}:{timestamp}"
    token = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
    return f"{token}:{timestamp}"


def validate_auth_token(api_key: str, token: str) -> bool:
    """
    Validates an authentication token.
    :param api_key: The API key of the user.
    :param token: The token to validate.
    :return: True if the token is valid, False otherwise.
    """
    parts = token.split(":")
    if len(parts) != 2:
        return False

    token_hash, timestamp = parts
    try:
        timestamp = int(timestamp)
    except ValueError:
        return False

    # Check token expiration
    if time.time() - timestamp > TOKEN_EXPIRATION:
        return False

    # Validate token using HMAC
    user_data = API_KEYS.get(api_key)
    if not user_data:
        return False

    expected_token = hmac.new(
        user_data["secret"].encode(),
        f"{api_key}:{timestamp}".encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_token, token_hash)


def require_auth(role: Optional[str] = None):
    """
    Decorator to enforce authentication and role-based access control.
    :param role: The required role for accessing the endpoint.
    :return: The decorated function.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            api_key = request.headers.get("X-API-KEY")
            auth_token = request.headers.get("Authorization")

            if not api_key or not auth_token:
                return jsonify({"error": "Missing API key or token"}), 401

            if not validate_auth_token(api_key, auth_token):
                return jsonify({"error": "Invalid or expired token"}), 401

            # Role-based access control
            user_data = API_KEYS.get(api_key)
            if role and user_data["role"] not in ["superadmin", role]:
                return jsonify({"error": "Access denied"}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator


# Example usage with Flask
if __name__ == "__main__":
    from flask import Flask # type: ignore

    app = Flask(__name__)

    @app.route("/secure-data", methods=["GET"])
    @require_auth(role="admin")
    def secure_data():
        """
        An example endpoint that requires authentication and the admin role.
        """
        return jsonify({"message": "This is secure data only for admins!"})

    @app.route("/generate-token", methods=["POST"])
    def generate_token():
        """
        Endpoint to generate an authentication token.
        :return: JSON response containing the generated token.
        """
        data = request.get_json()
        api_key = data.get("api_key")

        if not api_key or api_key not in API_KEYS:
            return jsonify({"error": "Invalid API key"}), 400

        token = generate_auth_token(api_key, API_KEYS[api_key]["secret"])
        return jsonify({"token": token})

    app.run(debug=True, port=5006)
