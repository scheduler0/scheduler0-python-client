"""
Credential management methods for Scheduler0 client.
"""

from typing import Optional
from .client import Client
from .types import (
    CredentialCreateRequestBody,
    CredentialUpdateRequestBody,
    CredentialDeleteRequestBody,
    CredentialArchiveRequestBody,
)


def list_credentials(
    self: Client,
    limit: int = 10,
    offset: int = 0,
    order_by: Optional[str] = None,
    order_by_direction: Optional[str] = None,
    account_id_override: Optional[str] = None,
) -> dict:
    """List credentials with pagination and ordering."""
    params = {
        "limit": str(limit),
        "offset": str(offset),
    }
    if order_by:
        params["orderBy"] = order_by
    if order_by_direction:
        params["orderByDirection"] = order_by_direction

    return self._get("/credentials", params=params, account_id_override=account_id_override)


def create_credential(
    self: Client,
    body: CredentialCreateRequestBody,
    account_id_override: Optional[str] = None,
) -> dict:
    """Create a new credential."""
    return self._post("/credentials", body, account_id_override=account_id_override)


def get_credential(
    self: Client,
    credential_id: str,
    account_id_override: Optional[str] = None,
) -> dict:
    """Get a specific credential."""
    return self._get(f"/credentials/{credential_id}", account_id_override=account_id_override)


def update_credential(
    self: Client,
    credential_id: str,
    body: CredentialUpdateRequestBody,
    account_id_override: Optional[str] = None,
) -> dict:
    """Update a credential."""
    return self._put(f"/credentials/{credential_id}", body, account_id_override=account_id_override)


def delete_credential(
    self: Client,
    credential_id: str,
    body: CredentialDeleteRequestBody,
    account_id_override: Optional[str] = None,
) -> None:
    """Delete a credential."""
    self._delete(f"/credentials/{credential_id}", body, account_id_override=account_id_override)


def archive_credential(
    self: Client,
    credential_id: str,
    body: CredentialArchiveRequestBody,
    account_id_override: Optional[str] = None,
) -> None:
    """Archive a credential."""
    self._post(f"/credentials/{credential_id}/archive", body, account_id_override=account_id_override)


# Attach methods to Client class
Client.list_credentials = list_credentials
Client.create_credential = create_credential
Client.get_credential = get_credential
Client.update_credential = update_credential
Client.delete_credential = delete_credential
Client.archive_credential = archive_credential

