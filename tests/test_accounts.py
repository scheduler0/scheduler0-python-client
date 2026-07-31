"""
Tests for account management methods.
"""

import pytest
from unittest.mock import patch, Mock
from scheduler0.types import AccountCreateRequestBody, AccountUpdateRequestBody, FeatureRequest


class TestAccounts:
    """Test account management methods."""

    @patch('scheduler0.client.Client._post')
    def test_create_account(self, mock_post, client):
        """Test creating an account."""
        mock_post.return_value = {"success": True, "data": {"id": 1, "name": "Test Account"}}
        body = AccountCreateRequestBody(name="Test Account")
        result = client.create_account(body)
        assert result["success"] is True
        mock_post.assert_called_once_with("/accounts", body, account_id_override=None)

    @patch('scheduler0.client.Client._get')
    def test_get_account(self, mock_get, client):
        """Test getting an account."""
        mock_get.return_value = {"success": True, "data": {"id": 1, "name": "Test Account"}}
        result = client.get_account("1")
        assert result["success"] is True
        mock_get.assert_called_once_with("/accounts/1", params=None, account_id_override=None)

    @patch('scheduler0.client.Client._put')
    def test_update_account(self, mock_put, client):
        """Test updating (renaming) an account."""
        mock_put.return_value = {"success": True, "data": {"id": 1, "name": "Renamed"}}
        body = AccountUpdateRequestBody(name="Renamed")
        result = client.update_account("1", body)
        assert result["success"] is True
        mock_put.assert_called_once_with("/accounts/1", body, account_id_override=None)

    @patch('scheduler0.client.Client._get')
    def test_get_ai_usage(self, mock_get, client):
        """Test getting the account's log-derived AI usage."""
        mock_get.return_value = {
            "success": True,
            "data": {
                "accountId": 123,
                "periodStart": "2025-01-01T00:00:00Z",
                "nextResetDate": "2025-02-01T00:00:00Z",
                "prompt": {"limit": 1000, "used": 50, "remaining": 950},
                "classify": {"limit": 1000, "used": 40, "remaining": 960},
                "estimatedCostUsd": 1.23,
            },
        }
        result = client.get_ai_usage("123")
        assert result["success"] is True
        mock_get.assert_called_once_with("/accounts/123/ai/usage", params=None, account_id_override="123")

    @patch('scheduler0.client.Client._put')
    def test_add_feature_to_account(self, mock_put, client):
        """Test adding a feature to an account."""
        mock_put.return_value = {"success": True, "data": {"featureId": 1}}
        body = FeatureRequest(feature_id=1)
        result = client.add_feature_to_account("1", body)
        assert result["success"] is True
        mock_put.assert_called_once_with("/accounts/1/feature", body, account_id_override="1")

    @patch('scheduler0.client.Client._delete')
    def test_remove_feature_from_account(self, mock_delete, client):
        """Test removing a feature from an account."""
        body = FeatureRequest(feature_id=1)
        client.remove_feature_from_account("1", body)
        mock_delete.assert_called_once_with("/accounts/1/feature", body, account_id_override="1")

    @patch('scheduler0.client.Client._request')
    def test_add_all_features_to_account(self, mock_request, client):
        """Test adding all features to an account."""
        mock_request.return_value.status_code = 204
        client.add_all_features_to_account("1")
        mock_request.assert_called_once_with(
            "PUT", "/accounts/1/features/all", None, params=None, account_id_override="1"
        )

    @patch('scheduler0.client.Client._request')
    def test_remove_all_features_from_account(self, mock_request, client):
        """Test removing all features from an account."""
        mock_request.return_value.status_code = 204
        client.remove_all_features_from_account("1")
        mock_request.assert_called_once_with(
            "DELETE", "/accounts/1/features/all", None, params=None, account_id_override="1"
        )

