import time
from typing import Dict, Any, List


def format_block(block: Dict[str, Any]) -> Dict[str, Any]:
    """
    Formats a block's details for better readability.
    :param block: The raw block data.
    :return: A formatted block dictionary.
    """
    return {
        "Block Number": block.get("number"),
        "Block Hash": block.get("hash"),
        "Timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(block.get("timestamp"))),
        "Transactions Count": len(block.get("transactions", [])),
        "Transactions": block.get("transactions", [])
    }


def format_transaction(transaction: Dict[str, Any]) -> Dict[str, Any]:
    """
    Formats a transaction's details for better readability.
    :param transaction: The raw transaction data.
    :return: A formatted transaction dictionary.
    """
    return {
        "Transaction Hash": transaction.get("hash"),
        "From": transaction.get("from"),
        "To": transaction.get("to"),
        "Amount": transaction.get("amount"),
        "Timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(transaction.get("timestamp")))
    }


def format_balance(address: str, balance: float) -> Dict[str, Any]:
    """
    Formats an account balance.
    :param address: The blockchain address.
    :param balance: The account balance.
    :return: A formatted balance dictionary.
    """
    return {
        "Address": address,
        "Balance": f"{balance:.4f} tokens"
    }


def format_transaction_history(history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Formats a list of transactions for better readability.
    :param history: The raw transaction history.
    :return: A list of formatted transaction dictionaries.
    """
    return [format_transaction(tx) for tx in history]


def human_readable_time(seconds: int) -> str:
    """
    Converts seconds to a human-readable format (days, hours, minutes, seconds).
    :param seconds: Time in seconds.
    :return: Human-readable time string.
    """
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    parts = [
        f"{days}d" if days else "",
        f"{hours}h" if hours else "",
        f"{minutes}m" if minutes else "",
        f"{seconds}s" if seconds else "",
    ]
    return " ".join(filter(bool, parts))


# Example usage
if __name__ == "__main__":
    # Mock data for demonstration
    block = {
        "number": 12345,
        "hash": "abcdef123456",
        "timestamp": 1673445600,
        "transactions": [
            {"hash": "tx1", "from": "address1", "to": "address2", "amount": 100, "timestamp": 1673445601},
            {"hash": "tx2", "from": "address3", "to": "address4", "amount": 200, "timestamp": 1673445602}
        ]
    }

    transaction = {
        "hash": "tx12345",
        "from": "address1",
        "to": "address2",
        "amount": 50,
        "timestamp": 1673445700
    }

    balance = 500.12345

    history = [
        {"hash": "tx1", "from": "address1", "to": "address2", "amount": 10.0, "timestamp": 1673445800},
        {"hash": "tx2", "from": "address3", "to": "address4", "amount": 20.0, "timestamp": 1673445900},
    ]

    # Format and display data
    print("Formatted Block:")
    print(format_block(block))

    print("\nFormatted Transaction:")
    print(format_transaction(transaction))

    print("\nFormatted Balance:")
    print(format_balance("address1", balance))

    print("\nFormatted Transaction History:")
    print(format_transaction_history(history))

    print("\nHuman-Readable Time:")
    print(human_readable_time(90061))  # 1 day, 1 hour, 1 minute, 1 second
