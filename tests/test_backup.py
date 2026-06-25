"""
Tests for backup and restore methods.
"""

import pytest
from unittest.mock import patch


class TestBackup:
    """Test backup and restore methods."""

    @patch('scheduler0.client.Client._post')
    def test_backup_database(self, mock_post, client):
        """Test starting a database backup."""
        mock_post.return_value = {
            "success": True,
            "data": {"status": "backup initiated"},
        }
        result = client.backup_database()
        assert result["success"] is True
        assert result["data"]["status"] == "backup initiated"
        mock_post.assert_called_once_with(
            "/cluster/backup", account_id_override=None
        )

    @patch('scheduler0.client.Client._post')
    def test_restore_database(self, mock_post, client):
        """Test restoring from a backup file."""
        mock_post.return_value = {
            "success": True,
            "data": {"status": "restore initiated", "requestId": "abc123"},
        }
        result = client.restore_database("db-20260212-114810.db")
        assert result["success"] is True
        assert result["data"]["requestId"] == "abc123"
        mock_post.assert_called_once_with(
            "/cluster/restore",
            {"filePath": "db-20260212-114810.db"},
            account_id_override=None,
        )
