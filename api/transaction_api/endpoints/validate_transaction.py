from flask import Flask, request, jsonify # type: ignore
from transaction_utils import verify_signature
import time

app = Flask(__name__)

@app.route("/validate_transaction", methods=["POST"])
def validate_transaction():
    """
    API endpoint to validate a transaction.
    Expected JSON input:
    {
        "id": "transaction_id",
        "sender": "address1",
        "receiver": "address2",
        "amount": 50.0,
        "timestamp": 1673445600,
        "signature": "transaction_signature",
        "public_key": "sender_public_key"
    }
    """
    transaction = request.json

    # Validate required fields
    required_fields = ["id", "sender", "receiver", "amount", "timestamp", "signature", "public_key"]
    for field in required_fields:
        if field not in transaction:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Validate transaction timestamp (not too old or from the future)
    current_time = time.time()
    if transaction["timestamp"] > current_time:
        return jsonify({"error": "Transaction timestamp is in the future"}), 400
    if current_time - transaction["timestamp"] > 3600:  # 1-hour validity window
        return jsonify({"error": "Transaction timestamp is too old"}), 400

    # Validate transaction amount
    if transaction["amount"] <= 0:
        return jsonify({"error": "Transaction amount must be greater than zero"}), 400

    # Verify transaction signature
    is_valid_signature = verify_signature(
        transaction["public_key"],
        transaction,
        transaction["signature"]
    )

    if not is_valid_signature:
        return jsonify({"error": "Invalid transaction signature"}), 400

    # If all validations pass
    return jsonify({"message": "Transaction is valid"}), 200


if __name__ == "__main__":
    app.run(debug=True)
