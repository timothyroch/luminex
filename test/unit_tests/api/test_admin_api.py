import unittest
from unittest.mock import patch, MagicMock
from api.admin_api.endpoints.manage_nodes import add_node, remove_node, list_nodes
from api.admin_api.endpoints.restart_node import restart_node
from api.admin_api.endpoints.diagnostics import run_diagnostics

class TestAdminAPI(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing the admin API.
        """
        self.node_url = "http://node1.blockchain.net"
        self.diagnostics_report = {
            "status": "success",
            "data": {
                "cpu_usage": "15%",
                "memory_usage": "1.5GB",
                "disk_space": "50GB free",
                "network_latency": "30ms"
            }
        }

    @patch("api.admin_api.endpoints.manage_nodes.NodeManager")
    def test_add_node(self, mock_node_manager):
        """
        Test adding a node to the network.
        """
        mock_node_manager().add_node.return_value = {"status": "success", "message": "Node added successfully"}
        response = add_node(self.node_url)
        self.assertEqual(response["status"], "success", "Failed to add node")
        self.assertEqual(response["message"], "Node added successfully", "Add node message mismatch")
        print("Add node test passed.")

    @patch("api.admin_api.endpoints.manage_nodes.NodeManager")
    def test_remove_node(self, mock_node_manager):
        """
        Test removing a node from the network.
        """
        mock_node_manager().remove_node.return_value = {"status": "success", "message": "Node removed successfully"}
        response = remove_node(self.node_url)
        self.assertEqual(response["status"], "success", "Failed to remove node")
        self.assertEqual(response["message"], "Node removed successfully", "Remove node message mismatch")
        print("Remove node test passed.")

    @patch("api.admin_api.endpoints.manage_nodes.NodeManager")
    def test_list_nodes(self, mock_node_manager):
        """
        Test listing all nodes in the network.
        """
        mock_node_manager().list_nodes.return_value = {"status": "success", "data": ["node1", "node2", "node3"]}
        response = list_nodes()
        self.assertEqual(response["status"], "success", "Failed to list nodes")
        self.assertIn("node1", response["data"], "Node1 not found in node list")
        print("List nodes test passed.")

    @patch("api.admin_api.endpoints.restart_node.NodeManager")
    def test_restart_node(self, mock_node_manager):
        """
        Test restarting a node.
        """
        mock_node_manager().restart_node.return_value = {"status": "success", "message": "Node restarted successfully"}
        response = restart_node(self.node_url)
        self.assertEqual(response["status"], "success", "Failed to restart node")
        self.assertEqual(response["message"], "Node restarted successfully", "Restart node message mismatch")
        print("Restart node test passed.")

    @patch("api.admin_api.endpoints.diagnostics.DiagnosticsRunner")
    def test_run_diagnostics(self, mock_diagnostics_runner):
        """
        Test running system diagnostics.
        """
        mock_diagnostics_runner().run.return_value = self.diagnostics_report
        response = run_diagnostics()
        self.assertEqual(response["status"], "success", "Failed to run diagnostics")
        self.assertIn("cpu_usage", response["data"], "CPU usage not found in diagnostics report")
        print("Run diagnostics test passed.")

if __name__ == "__main__":
    unittest.main()
