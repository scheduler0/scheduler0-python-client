"""
Tests for execution management methods.
"""

import pytest
from unittest.mock import patch


class TestExecutions:
    """Test execution management methods."""

    @patch('scheduler0.client.Client._get')
    def test_list_executions(self, mock_get, client):
        """Test listing executions."""
        mock_get.return_value = {
            "success": True,
            "data": {
                "total": 1,
                "executions": [{"id": 1, "jobId": 123}],
            },
        }
        result = client.list_executions(
            start_date="2024-01-01T00:00:00Z",
            end_date="2024-12-31T23:59:59Z",
            limit=10,
            offset=0,
        )
        assert result["success"] is True
        call_args = mock_get.call_args
        assert call_args[1]["params"]["startDate"] == "2024-01-01T00:00:00Z"
        assert call_args[1]["params"]["endDate"] == "2024-12-31T23:59:59Z"
        assert call_args[1]["params"]["limit"] == "10"

    @patch('scheduler0.client.Client._get')
    def test_list_executions_with_filters(self, mock_get, client):
        """Test listing executions with project and job filters."""
        client.list_executions(
            start_date="2024-01-01T00:00:00Z",
            end_date="2024-12-31T23:59:59Z",
            project_id=123,
            job_id=456,
            limit=10,
            offset=0,
        )
        call_args = mock_get.call_args
        assert call_args[1]["params"]["projectId"] == "123"
        assert call_args[1]["params"]["jobId"] == "456"

