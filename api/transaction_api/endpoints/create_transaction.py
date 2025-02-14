from flask import Flask, request, jsonify # type: ignore
from transaction_utils import generate_transaction_id, sign_transaction
import time

app = Flask(__name__)

# In-memory storage for simplicity (replace with a database in production)
transaction_pool = []

@app.route("/create_transaction", methods=["POST"])
def create_transaction():
    """
    API endpoint to create a new transaction.
    Expected JSON input:
    {
        "sender": "address1",
        "receiver": "address2",
        "amount": 50.0,
        "private_key": "sender_private_key"
    }
    """
    data = request.json

    # Validate input
    required_fields = ["sender", "receiver", "amount", "private_key"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Extract transaction details
    sender = data["sender"]
    receiver = data["receiver"]
    amount = data["amount"]
    private_key = data["private_key"]

    # Validate amount
    if amount <= 0:
        return jsonify({"error": "Transaction amount must be greater than zero"}), 400

    # Generate transaction
    transaction = {
        "id": generate_transaction_id(sender, receiver, amount, time.time()),
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "timestamp": time.time()
    }

    # Sign the transaction
    transaction_signature = sign_transaction(private_key, transaction)
    transaction["signature"] = transaction_signature

    # Add to transaction pool
    transaction_pool.append(transaction)

    return jsonify({
        "message": "Transaction created successfully",
        "transaction": transaction
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
