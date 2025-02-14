#!/bin/bash

# Configuration
NODES_DIR="testnet/nodes"
BASE_PORT=30303
RPC_BASE_PORT=8545
CHAIN_ID=12345
NODE_BINARY="blockchain_node"  # Replace with the actual blockchain node executable

# Function to start a node
start_node() {
    NODE_PATH=$1
    NODE_INDEX=$2
    P2P_PORT=$((BASE_PORT + NODE_INDEX))
    RPC_PORT=$((RPC_BASE_PORT + NODE_INDEX))

    echo "Starting node at $NODE_PATH with P2P port $P2P_PORT and RPC port $RPC_PORT..."

    nohup $NODE_BINARY \
        --datadir "$NODE_PATH" \
        --port $P2P_PORT \
        --rpc \
        --rpcport $RPC_PORT \
        --networkid $CHAIN_ID \
        --genesis "$NODE_PATH/genesis.json" \
        > "$NODE_PATH/node.log" 2>&1 &

    echo "Node $NODE_INDEX started. Logs can be found at $NODE_PATH/node.log"
}

# Start all nodes
NODE_INDEX=0
for NODE in "$NODES_DIR"/node_*; do
    if [ -d "$NODE" ]; then
        start_node "$NODE" $NODE_INDEX
        ((NODE_INDEX++))
    else
        echo "Warning: $NODE is not a valid directory, skipping..."
    fi
done

echo "All nodes started."
