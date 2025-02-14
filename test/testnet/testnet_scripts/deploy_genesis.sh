#!/bin/bash

# Configuration
NODES_DIR="testnet/nodes"
GENESIS_FILE="testnet/genesis.json"

# Check if genesis file exists
if [ ! -f "$GENESIS_FILE" ]; then
    echo "Error: Genesis file not found at $GENESIS_FILE"
    exit 1
fi

# Deploy genesis block to each node
echo "Deploying genesis block to nodes..."
for NODE in "$NODES_DIR"/node_*; do
    if [ -d "$NODE" ]; then
        cp "$GENESIS_FILE" "$NODE/genesis.json"
        echo "Genesis block deployed to $NODE"
    else
        echo "Warning: $NODE is not a valid directory, skipping..."
    fi
done

echo "Genesis block deployment completed."
