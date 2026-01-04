"""
Account management methods for Scheduler0 client.
"""

from typing import Optional
from .client import Client
from .types import AccountCreateRequestBody, FeatureRequest


def create_account(self: Client, body: AccountCreateRequestBody) -> dict:
    """Create a new account."""
    return self._post("/accounts", body, account_id_override=None)


def get_account(self: Client, account_id: str) -> dict:
    """Get account details by ID."""
    return self._get(f"/accounts/{account_id}", params=None, account_id_override=None)


def add_feature_to_account(self: Client, account_id: str, body: FeatureRequest) -> dict:
    """Add a feature to an account."""
    return self._put(f"/accounts/{account_id}/feature", body, account_id_override=account_id)


def remove_feature_from_account(self: Client, account_id: str, body: FeatureRequest) -> None:
    """Remove a feature from an account."""
    self._delete(f"/accounts/{account_id}/feature", body, account_id_override=account_id)


def add_all_features_to_account(self: Client, account_id: str) -> None:
    """Add all features to an account."""
    self._request("PUT", f"/accounts/{account_id}/features/all", None, params=None, account_id_override=account_id)


def remove_all_features_from_account(self: Client, account_id: str) -> None:
    """Remove all features from an account."""
    self._request("DELETE", f"/accounts/{account_id}/features/all", None, params=None, account_id_override=account_id)


def get_account_execution_count(self: Client, account_id: str) -> dict:
    """Get execution count for an account."""
    return self._get(f"/accounts/{account_id}/execution-count", params=None, account_id_override=account_id)


def increase_account_execution_count(self: Client, account_id: str, count: int) -> dict:
    """Increase execution count for an account."""
    body = {"count": count}
    return self._put(f"/accounts/{account_id}/execution-count", body, account_id_override=account_id)


# Attach methods to Client class
Client.create_account = create_account
Client.get_account = get_account
Client.add_feature_to_account = add_feature_to_account
Client.remove_feature_from_account = remove_feature_from_account
Client.add_all_features_to_account = add_all_features_to_account
Client.remove_all_features_from_account = remove_all_features_from_account
Client.get_account_execution_count = get_account_execution_count
Client.increase_account_execution_count = increase_account_execution_count

