// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RollupContract {
    struct RollupBatch {
        bytes32 batchHash;
        uint256 transactionCount;
        uint256 timestamp;
    }

    address public owner;
    mapping(bytes32 => bool) public verifiedBatches;
    RollupBatch[] public batches;

    event BatchSubmitted(bytes32 indexed batchHash, uint256 transactionCount, uint256 timestamp);
    event ProofVerified(bytes32 indexed batchHash, bool success);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function submitBatch(bytes32 batchHash, uint256 transactionCount) external onlyOwner {
        require(!verifiedBatches[batchHash], "Batch already submitted");

        RollupBatch memory newBatch = RollupBatch({
            batchHash: batchHash,
            transactionCount: transactionCount,
            timestamp: block.timestamp
        });

        batches.push(newBatch);
        emit BatchSubmitted(batchHash, transactionCount, block.timestamp);
    }

    function verifyProof(bytes32 batchHash, bool proofValid) external onlyOwner {
        require(!verifiedBatches[batchHash], "Batch already verified");

        if (proofValid) {
            verifiedBatches[batchHash] = true;
            emit ProofVerified(batchHash, true);
        } else {
            emit ProofVerified(batchHash, false);
        }
    }

    function getBatchCount() external view returns (uint256) {
        return batches.length;
    }

    function getBatchByIndex(uint256 index) external view returns (bytes32, uint256, uint256) {
        require(index < batches.length, "Invalid index");

        RollupBatch memory batch = batches[index];
        return (batch.batchHash, batch.transactionCount, batch.timestamp);
    }

    function isBatchVerified(bytes32 batchHash) external view returns (bool) {
        return verifiedBatches[batchHash];
    }
}
