"""
Executor management methods for Scheduler0 client.
"""

from typing import Optional
from .client import Client
from .types import ExecutorRequestBody, ExecutorUpdateRequestBody, ExecutorDeleteRequestBody


def list_executors(
    self: Client,
    limit: int = 10,
    offset: int = 0,
    order_by: Optional[str] = None,
    order_by_direction: Optional[str] = None,
    account_id_override: Optional[str] = None,
) -> dict:
    """List executors with pagination and ordering."""
    params = {
        "limit": str(limit),
        "offset": str(offset),
    }
    if order_by:
        params["orderBy"] = order_by
    if order_by_direction:
        params["orderByDirection"] = order_by_direction

    return self._get("/executors", params=params, account_id_override=account_id_override)


def create_executor(
    self: Client,
    body: ExecutorRequestBody,
    account_id_override: Optional[str] = None,
) -> dict:
    """Create a new executor."""
    return self._post("/executors", body, account_id_override=account_id_override)


def get_executor(
    self: Client,
    executor_id: str,
    account_id_override: Optional[str] = None,
) -> dict:
    """Get a specific executor."""
    return self._get(f"/executors/{executor_id}", params=None, account_id_override=account_id_override)


def update_executor(
    self: Client,
    executor_id: str,
    body: ExecutorUpdateRequestBody,
    account_id_override: Optional[str] = None,
) -> dict:
    """Update an executor."""
    return self._put(f"/executors/{executor_id}", body, account_id_override=account_id_override)


def delete_executor(
    self: Client,
    executor_id: str,
    body: ExecutorDeleteRequestBody,
    account_id_override: Optional[str] = None,
) -> None:
    """Delete an executor."""
    self._delete(f"/executors/{executor_id}", body, account_id_override=account_id_override)


# Attach methods to Client class
Client.list_executors = list_executors
Client.create_executor = create_executor
Client.get_executor = get_executor
Client.update_executor = update_executor
Client.delete_executor = delete_executor

