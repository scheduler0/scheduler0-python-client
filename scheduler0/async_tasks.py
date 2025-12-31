"""
Async task management methods for Scheduler0 client.
"""

from typing import Optional
from .client import Client


def get_async_task(
    self: Client,
    request_id: str,
    account_id_override: Optional[str] = None,
) -> dict:
    """Get async task status by request ID."""
    return self._get(f"/async-tasks/{request_id}", params=None, account_id_override=account_id_override)


# Attach methods to Client class
Client.get_async_task = get_async_task

