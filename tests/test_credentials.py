"""
Tests for credential management methods.
"""

import pytest
from unittest.mock import patch
from scheduler0.types import (
    CredentialCreateRequestBody,
    CredentialUpdateRequestBody,
    CredentialDeleteRequestBody,
    CredentialArchiveRequestBody,
)


class TestCredentials:
    """Test credential management methods."""

    @patch('scheduler0.client.Client._get')
    def test_list_credentials(self, mock_get, client):
        """Test listing credentials."""
        mock_get.return_value = {
            "success": True,
            "data": {
                "total": 1,
                "credentials": [{"id": 1, "apiKey": "key"}],
            },
        }
        result = client.list_credentials(limit=10, offset=0)
        assert result["success"] is True
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[0][0] == "/credentials"
        assert call_args[1]["params"]["limit"] == "10"
        assert call_args[1]["params"]["offset"] == "0"

    @patch('scheduler0.client.Client._get')
    def test_list_credentials_with_ordering(self, mock_get, client):
        """Test listing credentials with ordering."""
        client.list_credentials(
            limit=10,
            offset=0,
            order_by="date_created",
            order_by_direction="desc",
        )
        call_args = mock_get.call_args
        assert call_args[1]["params"]["orderBy"] == "date_created"
        assert call_args[1]["params"]["orderByDirection"] == "desc"

    @patch('scheduler0.client.Client._post')
    def test_create_credential(self, mock_post, client):
        """Test creating a credential."""
        mock_post.return_value = {"success": True, "data": {"id": 1, "apiKey": "key"}}
        body = CredentialCreateRequestBody(created_by="user@example.com")
        result = client.create_credential(body)
        assert result["success"] is True
        mock_post.assert_called_once_with("/credentials", body, account_id_override=None)

    @patch('scheduler0.client.Client._get')
    def test_get_credential(self, mock_get, client):
        """Test getting a credential."""
        mock_get.return_value = {"success": True, "data": {"id": 1, "apiKey": "key"}}
        result = client.get_credential("1")
        assert result["success"] is True
        mock_get.assert_called_once_with("/credentials/1", params=None, account_id_override=None)

    @patch('scheduler0.client.Client._put')
    def test_update_credential(self, mock_put, client):
        """Test updating a credential."""
        mock_put.return_value = {"success": True, "data": {"id": 1}}
        body = CredentialUpdateRequestBody(modified_by="user@example.com", archived=False)
        result = client.update_credential("1", body)
        assert result["success"] is True
        mock_put.assert_called_once_with("/credentials/1", body, account_id_override=None)

    @patch('scheduler0.client.Client._delete')
    def test_delete_credential(self, mock_delete, client):
        """Test deleting a credential."""
        body = CredentialDeleteRequestBody(deleted_by="user@example.com")
        client.delete_credential("1", body)
        mock_delete.assert_called_once_with("/credentials/1", body, account_id_override=None)

    @patch('scheduler0.client.Client._post')
    def test_archive_credential(self, mock_post, client):
        """Test archiving a credential."""
        body = CredentialArchiveRequestBody(archived_by="user@example.com")
        client.archive_credential("1", body)
        mock_post.assert_called_once_with("/credentials/1/archive", body, account_id_override=None)

