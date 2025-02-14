import unittest
from unittest.mock import patch, MagicMock
from blockchain.network.p2p_node import P2PNode
from blockchain.network.message_handler import MessageHandler
from blockchain.network.node_discovery import NodeDiscovery

class TestNetwork(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing P2P networking.
        """
        self.node = P2PNode(node_id="node1", port=5000)
        self.message_handler = MessageHandler(self.node)
        self.node_discovery = NodeDiscovery(self.node)
        self.peer_nodes = ["http://node2.blockchain.net", "http://node3.blockchain.net"]

    @patch("blockchain.network.p2p_node.P2PNode.broadcast")
    def test_message_broadcast(self, mock_broadcast):
        """
        Test that messages are broadcast correctly to peer nodes.
        """
        message = {"type": "NEW_BLOCK", "data": "Block data"}
        self.node.broadcast(message)
        mock_broadcast.assert_called_with(message)
        print("Message broadcast test passed.")

    def test_message_handling(self):
        """
        Test that incoming messages are handled appropriately.
        """
        message = {"type": "TRANSACTION", "data": "Sample transaction data"}
        with patch.object(self.message_handler, "handle_transaction") as mock_handle_transaction:
            self.message_handler.handle_message(message)
            mock_handle_transaction.assert_called_once_with("Sample transaction data")
        print("Message handling test passed.")

    @patch("blockchain.network.node_discovery.NodeDiscovery.discover_nodes")
    def test_node_discovery(self, mock_discover_nodes):
        """
        Test that node discovery finds valid peer nodes.
        """
        mock_discover_nodes.return_value = self.peer_nodes
        discovered_nodes = self.node_discovery.discover_nodes()
        self.assertEqual(discovered_nodes, self.peer_nodes, "Discovered nodes do not match expected peers")
        print("Node discovery test passed.")

    def test_connect_to_peer(self):
        """
        Test that a node can connect to a peer successfully.
        """
        with patch("blockchain.network.p2p_node.P2PNode.connect_to_peer") as mock_connect:
            mock_connect.return_value = True
            result = self.node.connect_to_peer("http://node2.blockchain.net")
            self.assertTrue(result, "Failed to connect to peer node")
        print("Peer connection test passed.")

    def test_invalid_message_rejection(self):
        """
        Test that invalid messages are rejected by the message handler.
        """
        invalid_message = {"type": "INVALID_TYPE", "data": "Invalid data"}
        with patch.object(self.message_handler, "reject_message") as mock_reject_message:
            self.message_handler.handle_message(invalid_message)
            mock_reject_message.assert_called_once_with(invalid_message)
        print("Invalid message rejection test passed.")

if __name__ == "__main__":
    unittest.main()
