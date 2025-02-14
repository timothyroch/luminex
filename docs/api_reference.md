

### `api_reference.md`

# API Reference Documentation

This document provides an overview of all available API endpoints in the blockchain system, including their request and response structures.

---

## **Transaction API**

### 1. Create Transaction
**Endpoint**: `POST /api/transaction_api/endpoints/create_transaction`

- **Description**: Creates a new transaction and returns the transaction hash.

- **Request Payload**:
  ```json
  {
    "sender": "0x123abc456def...",
    "receiver": "0x789ghi012jkl...",
    "amount": 100,
    "fee": 0.01,
    "signature": "0xabcdef..."
  }
  ```

- **Response**:
  ```json
  {
    "status": "success",
    "transaction_hash": "0x123456789abcdef..."
  }
  ```

---

### 2. Broadcast Transaction
**Endpoint**: `POST /api/transaction_api/endpoints/broadcast_transaction`

- **Description**: Broadcasts a signed transaction to the network.

- **Request Payload**:
  ```json
  {
    "transaction_data": {
      "sender": "0x123abc456def...",
      "receiver": "0x789ghi012jkl...",
      "amount": 100,
      "fee": 0.01,
      "signature": "0xabcdef..."
    }
  }
  ```

- **Response**:
  ```json
  {
    "status": "success",
    "message": "Transaction broadcasted successfully"
  }
  ```

---

### 3. Validate Transaction
**Endpoint**: `POST /api/transaction_api/endpoints/validate_transaction`

- **Description**: Validates a transaction before submission.

- **Request Payload**:
  ```json
  {
    "transaction_data": {
      "sender": "0x123abc456def...",
      "receiver": "0x789ghi012jkl...",
      "amount": 100,
      "fee": 0.01,
      "signature": "0xabcdef..."
    }
  }
  ```

- **Response**:
  ```json
  {
    "status": "valid",
    "message": "Transaction is valid"
  }
  ```

---

## **Explorer API**

### 1. Query Block
**Endpoint**: `GET /api/explorer_api/endpoints/query_block/{block_hash}`

- **Description**: Fetches details of a block using its hash.

- **Response**:
  ```json
  {
    "block_hash": "0xabcdef...",
    "height": 10234,
    "transactions": [
      "0x123456...",
      "0x789abc..."
    ],
    "timestamp": "2025-01-10T10:00:00Z"
  }
  ```

---

### 2. Query Address
**Endpoint**: `GET /api/explorer_api/endpoints/query_address/{address}`

- **Description**: Fetches balance and transaction history for a specific address.

- **Response**:
  ```json
  {
    "address": "0x123abc456def...",
    "balance": 500.5,
    "transactions": [
      "0x123456...",
      "0x789abc..."
    ]
  }
  ```

---

### 3. Query Transaction
**Endpoint**: `GET /api/explorer_api/endpoints/query_transaction/{transaction_hash}`

- **Description**: Fetches details of a specific transaction.

- **Response**:
  ```json
  {
    "transaction_hash": "0x123456789abcdef...",
    "sender": "0x123abc456def...",
    "receiver": "0x789ghi012jkl...",
    "amount": 100,
    "fee": 0.01,
    "status": "confirmed",
    "timestamp": "2025-01-10T10:10:00Z"
  }
  ```

---

## **Healthcheck API**

### 1. Node Status
**Endpoint**: `GET /api/healthcheck_api/endpoints/node_status`

- **Description**: Returns the status of blockchain nodes.

- **Response**:
  ```json
  {
    "status": "online",
    "node_count": 10,
    "synced": true
  }
  ```

---

### 2. Block Sync Status
**Endpoint**: `GET /api/healthcheck_api/endpoints/block_sync_status`

- **Description**: Checks the synchronization status of the blockchain.

- **Response**:
  ```json
  {
    "latest_block_height": 10234,
    "synced": true,
    "node_status": [
      {
        "node_id": "node1",
        "status": "synced"
      },
      {
        "node_id": "node2",
        "status": "syncing"
      }
    ]
  }
  ```

---

### 3. Network Health
**Endpoint**: `GET /api/healthcheck_api/endpoints/network_health`

- **Description**: Assesses the overall health of the network.

- **Response**:
  ```json
  {
    "latency_ms": 50,
    "packet_loss": 0.01,
    "status": "healthy"
  }
  ```

---

## **Admin API**

### 1. Manage Nodes
**Endpoint**: `POST /api/admin_api/endpoints/manage_nodes`

- **Description**: Adds or removes nodes from the network.

- **Request Payload**:
  ```json
  {
    "action": "add",
    "node_id": "node3",
    "address": "192.168.1.3"
  }
  ```

- **Response**:
  ```json
  {
    "status": "success",
    "message": "Node added successfully"
  }
  ```

---

### 2. Restart Node
**Endpoint**: `POST /api/admin_api/endpoints/restart_node`

- **Description**: Restarts a specific node.

- **Request Payload**:
  ```json
  {
    "node_id": "node2"
  }
  ```

- **Response**:
  ```json
  {
    "status": "success",
    "message": "Node restarted successfully"
  }
  ```

---

### 3. Diagnostics
**Endpoint**: `GET /api/admin_api/endpoints/diagnostics`

- **Description**: Retrieves system diagnostics for a specific node.

- **Response**:
  ```json
  {
    "node_id": "node1",
    "cpu_usage": 50,
    "memory_usage": 60,
    "disk_space": 80,
    "network_latency": 10
  }
  ```

---

## **Common HTTP Status Codes**

| Status Code | Description                     |
|-------------|---------------------------------|
| 200         | Success                         |
| 400         | Bad Request                     |
| 401         | Unauthorized                    |
| 404         | Not Found                       |
| 500         | Internal Server Error           |

---

### Notes
- All endpoints use HTTPS for secure communication.
- API keys are required for authentication.

