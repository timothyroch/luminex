// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PlasmaContract {
    struct Commitment {
        bytes32 blockHash;
        uint256 blockNumber;
        uint256 timestamp;
    }

    struct ExitRequest {
        address user;
        uint256 amount;
        uint256 blockNumber;
        bool finalized;
    }

    address public operator;
    mapping(bytes32 => bool) public committedBlocks;
    mapping(address => uint256) public balances;
    mapping(bytes32 => ExitRequest) public exits;

    event BlockCommitted(bytes32 indexed blockHash, uint256 blockNumber, uint256 timestamp);
    event ExitRequested(address indexed user, uint256 amount, uint256 blockNumber, bytes32 exitHash);
    event ExitFinalized(address indexed user, uint256 amount, uint256 blockNumber);

    modifier onlyOperator() {
        require(msg.sender == operator, "Not authorized");
        _;
    }

    constructor() {
        operator = msg.sender;
    }

    function commitBlock(bytes32 blockHash, uint256 blockNumber) external onlyOperator {
        require(!committedBlocks[blockHash], "Block already committed");

        committedBlocks[blockHash] = true;
        emit BlockCommitted(blockHash, blockNumber, block.timestamp);
    }

    function requestExit(uint256 amount, uint256 blockNumber) external {
        require(amount > 0, "Invalid amount");
        bytes32 exitHash = keccak256(abi.encodePacked(msg.sender, amount, blockNumber));
        require(exits[exitHash].user == address(0), "Exit already requested");

        exits[exitHash] = ExitRequest({
            user: msg.sender,
            amount: amount,
            blockNumber: blockNumber,
            finalized: false
        });

        emit ExitRequested(msg.sender, amount, blockNumber, exitHash);
    }

    function finalizeExit(bytes32 exitHash) external {
        ExitRequest storage exitRequest = exits[exitHash];
        require(exitRequest.user != address(0), "Invalid exit request");
        require(!exitRequest.finalized, "Exit already finalized");
        require(committedBlocks[keccak256(abi.encodePacked(exitRequest.blockNumber))], "Block not committed");

        exitRequest.finalized = true;
        balances[exitRequest.user] += exitRequest.amount;

        emit ExitFinalized(exitRequest.user, exitRequest.amount, exitRequest.blockNumber);
    }

    function withdraw() external {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "No funds to withdraw");

        balances[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }

    // Allow contract to receive Ether for test purposes
    receive() external payable {}
}
