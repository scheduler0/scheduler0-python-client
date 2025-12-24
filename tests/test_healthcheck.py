"""
Tests for healthcheck methods.
"""

import pytest
from unittest.mock import patch


class TestHealthcheck:
    """Test healthcheck methods."""

    @patch('scheduler0.client.Client._get')
    def test_healthcheck(self, mock_get, client):
        """Test healthcheck."""
        mock_get.return_value = {
            "success": True,
            "data": {
                "leaderAddress": "localhost:7070",
                "leaderId": "1",
                "raftStats": {
                    "state": "Leader",
                    "term": "1",
                },
            },
        }
        result = client.healthcheck()
        assert result["success"] is True
        assert result["data"]["leaderAddress"] == "localhost:7070"
        mock_get.assert_called_once_with("/healthcheck", params=None, account_id_override=None)

