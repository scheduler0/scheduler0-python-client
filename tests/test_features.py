"""
Tests for feature management methods.
"""

import pytest
from unittest.mock import patch


class TestFeatures:
    """Test feature management methods."""

    @patch('scheduler0.client.Client._get')
    def test_list_features(self, mock_get, client):
        """Test listing features."""
        mock_get.return_value = {
            "success": True,
            "data": [
                {"id": 1, "name": "feature1"},
                {"id": 2, "name": "feature2"},
            ],
        }
        result = client.list_features()
        assert result["success"] is True
        assert len(result["data"]) == 2
        mock_get.assert_called_once_with("/features", params=None, account_id_override=None)

