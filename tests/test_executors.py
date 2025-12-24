"""
Tests for executor management methods.
"""

import pytest
from unittest.mock import patch
from scheduler0.types import (
    ExecutorRequestBody,
    ExecutorUpdateRequestBody,
    ExecutorDeleteRequestBody,
)


class TestExecutors:
    """Test executor management methods."""

    @patch('scheduler0.client.Client._get')
    def test_list_executors(self, mock_get, client):
        """Test listing executors."""
        mock_get.return_value = {
            "success": True,
            "data": {
                "total": 1,
                "executors": [{"id": 1, "name": "webhook-executor"}],
            },
        }
        result = client.list_executors(limit=10, offset=0)
        assert result["success"] is True
        call_args = mock_get.call_args
        assert call_args[1]["params"]["limit"] == "10"

    @patch('scheduler0.client.Client._post')
    def test_create_executor_webhook(self, mock_post, client):
        """Test creating a webhook executor."""
        mock_post.return_value = {"success": True, "data": {"id": 1}}
        body = ExecutorRequestBody(
            name="webhook-executor",
            type="webhook_url",
            webhook_url="https://example.com/webhook",
            webhook_method="POST",
            webhook_secret="secret",
            created_by="user@example.com",
        )
        result = client.create_executor(body)
        assert result["success"] is True
        mock_post.assert_called_once_with("/executors", body, account_id_override=None)

    @patch('scheduler0.client.Client._post')
    def test_create_executor_cloud_function(self, mock_post, client):
        """Test creating a cloud function executor."""
        mock_post.return_value = {"success": True, "data": {"id": 1}}
        body = ExecutorRequestBody(
            name="cloud-function-executor",
            type="cloud_function",
            region="us-west-1",
            cloud_provider="aws",
            cloud_resource_url="https://example.com/function",
            cloud_api_key="api-key",
            cloud_api_secret="api-secret",
            created_by="user@example.com",
        )
        result = client.create_executor(body)
        assert result["success"] is True

    @patch('scheduler0.client.Client._get')
    def test_get_executor(self, mock_get, client):
        """Test getting an executor."""
        mock_get.return_value = {"success": True, "data": {"id": 1, "name": "executor"}}
        result = client.get_executor("1")
        assert result["success"] is True
        mock_get.assert_called_once_with("/executors/1", params=None, account_id_override=None)

    @patch('scheduler0.client.Client._put')
    def test_update_executor(self, mock_put, client):
        """Test updating an executor."""
        mock_put.return_value = {"success": True, "data": {"id": 1}}
        body = ExecutorUpdateRequestBody(
            name="updated-executor",
            type="webhook_url",
            modified_by="user@example.com",
        )
        result = client.update_executor("1", body)
        assert result["success"] is True
        mock_put.assert_called_once_with("/executors/1", body, account_id_override=None)

    @patch('scheduler0.client.Client._delete')
    def test_delete_executor(self, mock_delete, client):
        """Test deleting an executor."""
        body = ExecutorDeleteRequestBody(deleted_by="user@example.com")
        client.delete_executor("1", body)
        mock_delete.assert_called_once_with("/executors/1", body, account_id_override=None)

