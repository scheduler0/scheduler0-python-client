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

    @patch('scheduler0.client.Client._get')
    def test_list_executions_without_dates(self, mock_get, client):
        """Test listing executions without date filters."""
        mock_get.return_value = {
            "success": True,
            "data": {
                "total": 1,
                "executions": [{"id": 1, "jobId": 123}],
            },
        }
        client.list_executions(
            limit=10,
            offset=0,
        )
        call_args = mock_get.call_args
        assert "startDate" not in call_args[1]["params"]
        assert "endDate" not in call_args[1]["params"]
        assert call_args[1]["params"]["limit"] == "10"

    @patch('scheduler0.client.Client._get')
    def test_list_executions_with_state_and_ordering(self, mock_get, client):
        """Test listing executions with state filter and ordering."""
        mock_get.return_value = {
            "success": True,
            "data": {
                "total": 1,
                "executions": [{"id": 1, "jobId": 123}],
            },
        }
        client.list_executions(
            limit=10,
            offset=0,
            state="completed",
            order_by="dateCreated",
            order_direction="DESC",
        )
        call_args = mock_get.call_args
        assert call_args[1]["params"]["state"] == "completed"
        assert call_args[1]["params"]["orderBy"] == "dateCreated"
        assert call_args[1]["params"]["orderDirection"] == "DESC"

    @patch('scheduler0.client.Client._get')
    def test_get_date_range_analytics(self, mock_get, client):
        """Test getting date range analytics."""
        mock_get.return_value = {
            "success": True,
            "data": {
                "accountId": 123,
                "timezone": "UTC",
                "startDate": "2025-01-01",
                "startTime": "00:00:00",
                "endDate": "2025-01-01",
                "endTime": "23:59:59",
                "points": [
                    {
                        "date": "2025-01-01",
                        "time": "00:00:00",
                        "scheduled": 10,
                        "success": 8,
                        "failed": 2,
                    }
                ],
            },
        }
        result = client.get_date_range_analytics(
            start_date="2025-01-01",
            start_time="00:00:00",
            account_id=123,
        )
        assert result["success"] is True
        call_args = mock_get.call_args
        assert call_args[0][0] == "/executions/analytics"
        assert call_args[1]["params"]["startDate"] == "2025-01-01"
        assert call_args[1]["params"]["startTime"] == "00:00:00"

    @patch('scheduler0.client.Client._get')
    def test_get_execution_totals(self, mock_get, client):
        """Test getting execution totals."""
        mock_get.return_value = {
            "success": True,
            "data": {
                "accountId": 123,
                "scheduled": 100,
                "success": 80,
                "failed": 20,
            },
        }
        result = client.get_execution_totals(account_id=123)
        assert result["success"] is True
        assert result["data"]["scheduled"] == 100
        assert result["data"]["success"] == 80
        assert result["data"]["failed"] == 20
        call_args = mock_get.call_args
        assert call_args[0][0] == "/executions/totals"

    @patch('scheduler0.client.Client._post')
    def test_cleanup_old_execution_logs(self, mock_post, client):
        """Test cleaning up old execution logs."""
        mock_post.return_value = {
            "success": True,
            "data": {
                "message": "Old execution logs cleaned up successfully for account 123",
            },
        }
        result = client.cleanup_old_execution_logs(
            account_id="123",
            retention_months=6,
        )
        assert result["success"] is True
        assert "cleaned up successfully" in result["data"]["message"]
        call_args = mock_post.call_args
        assert call_args[0][0] == "/executions/cleanup-old-logs"
        assert call_args[1]["body"]["accountId"] == "123"
        assert call_args[1]["body"]["retentionMonths"] == 6

