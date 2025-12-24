"""
Tests for async task management methods.
"""

import pytest
from unittest.mock import patch


class TestAsyncTasks:
    """Test async task management methods."""

    @patch('scheduler0.client.Client._get')
    def test_get_async_task(self, mock_get, client):
        """Test getting an async task."""
        mock_get.return_value = {
            "success": True,
            "data": {
                "id": 1,
                "requestId": "req-123",
                "state": 1,
            },
        }
        result = client.get_async_task("req-123")
        assert result["success"] is True
        assert result["data"]["requestId"] == "req-123"
        mock_get.assert_called_once_with(
            "/async-tasks/req-123", params=None, account_id_override=None
        )

