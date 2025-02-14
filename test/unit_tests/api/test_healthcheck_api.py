import unittest
from unittest.mock import patch, MagicMock
from api.healthcheck_api.endpoints.node_status import get_node_status
from api.healthcheck_api.endpoints.block_sync_status import get_block_sync_status
from api.healthcheck_api.endpoints.network_health import get_network_health

class TestHealthcheckAPI(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing healthcheck API endpoints.
        """
        self.node_status_response = {
            "status": "success",
            "data": {
                "node_id": "node1",
                "uptime": "48 hours",
                "is_syncing": False,
                "current_block": 1200
            }
        }
        self.block_sync_status_response = {
            "status": "success",
            "data": {
                "synced_blocks": 1200,
                "total_blocks": 1200,
                "is_synced": True
            }
        }
        self.network_health_response = {
            "status": "success",
            "data": {
                "connected_peers": 8,
                "average_latency": 50,
                "is_healthy": True
            }
        }

    @patch("api.healthcheck_api.endpoints.node_status.NodeStatusChecker")
    def test_get_node_status(self, mock_checker):
        """
        Test the node status endpoint.
        """
        mock_checker().check_node_status.return_value = self.node_status_response
        response = get_node_status()
        self.assertEqual(response["status"], "success", "Failed to fetch node status")
        self.assertFalse(response["data"]["is_syncing"], "Node should not be syncing")
        print("Node status test passed.")

    @patch("api.healthcheck_api.endpoints.block_sync_status.BlockSyncChecker")
    def test_get_block_sync_status(self, mock_checker):
        """
        Test the block synchronization status endpoint.
        """
        mock_checker().check_sync_status.return_value = self.block_sync_status_response
        response = get_block_sync_status()
        self.assertEqual(response["status"], "success", "Failed to fetch block sync status")
        self.assertTrue(response["data"]["is_synced"], "Blocks should be fully synced")
        print("Block sync status test passed.")

    @patch("api.healthcheck_api.endpoints.network_health.NetworkHealthChecker")
    def test_get_network_health(self, mock_checker):
        """
        Test the network health endpoint.
        """
        mock_checker().check_network_health.return_value = self.network_health_response
        response = get_network_health()
        self.assertEqual(response["status"], "success", "Failed to fetch network health")
        self.assertTrue(response["data"]["is_healthy"], "Network should be healthy")
        print("Network health test passed.")

    @patch("api.healthcheck_api.endpoints.block_sync_status.BlockSyncChecker")
    def test_unsynced_blocks(self, mock_checker):
        """
        Test that the block sync status reports unsynced blocks correctly.
        """
        mock_checker().check_sync_status.return_value = {
            "status": "success",
            "data": {
                "synced_blocks": 1000,
                "total_blocks": 1200,
                "is_synced": False
            }
        }
        response = get_block_sync_status()
        self.assertFalse(response["data"]["is_synced"], "Sync status should report unsynced blocks")
        print("Unsynced blocks test passed.")

if __name__ == "__main__":
    unittest.main()
