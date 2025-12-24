"""
Execution management methods for Scheduler0 client.
"""

from typing import Optional
from .client import Client


def list_executions(
    self: Client,
    start_date: str,
    end_date: str,
    project_id: int = 0,
    job_id: int = 0,
    limit: int = 10,
    offset: int = 0,
    account_id_override: Optional[str] = None,
) -> dict:
    """
    List job executions with date filtering.

    Args:
        start_date: Start date for filtering (RFC3339 format, required)
        end_date: End date for filtering (RFC3339 format, required)
        project_id: Project ID to filter by (0 for all)
        job_id: Job ID to filter by (0 for all)
        limit: Maximum number of items to return
        offset: Number of items to skip
        account_id_override: Optional account ID override
    """
    params = {
        "startDate": start_date,
        "endDate": end_date,
        "projectId": str(project_id),
        "jobId": str(job_id),
        "limit": str(limit),
        "offset": str(offset),
    }

    return self._get("/executions", params=params, account_id_override=account_id_override)


# Attach methods to Client class
Client.list_executions = list_executions

