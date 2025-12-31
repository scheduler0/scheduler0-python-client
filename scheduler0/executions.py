"""
Execution management methods for Scheduler0 client.
"""

from typing import Optional, Literal
from .client import Client


def list_executions(
    self: Client,
    limit: int = 10,
    offset: int = 0,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    project_id: Optional[int] = None,
    job_id: Optional[int] = None,
    state: Optional[Literal["scheduled", "completed", "failed"]] = None,
    order_by: Optional[Literal["dateCreated", "lastExecutionDateTime", "nextExecutionDateTime"]] = None,
    order_direction: Optional[Literal["ASC", "DESC"]] = None,
    account_id_override: Optional[str] = None,
) -> dict:
    """
    List job executions with optional filtering and ordering.

    Args:
        limit: Maximum number of items to return
        offset: Number of items to skip
        start_date: Start date for filtering (RFC3339 format, optional)
        end_date: End date for filtering (RFC3339 format, optional)
        project_id: Project ID to filter by (optional)
        job_id: Job ID to filter by (optional)
        state: Execution state to filter by - "scheduled", "completed", or "failed" (optional)
        order_by: Field to order results by - "dateCreated", "lastExecutionDateTime", or "nextExecutionDateTime" (optional)
        order_direction: Direction to order results - "ASC" or "DESC" (optional)
        account_id_override: Optional account ID override
    """
    params = {
        "limit": str(limit),
        "offset": str(offset),
    }
    
    if start_date:
        params["startDate"] = start_date
    if end_date:
        params["endDate"] = end_date
    if project_id is not None:
        params["projectId"] = str(project_id)
    if job_id is not None:
        params["jobId"] = str(job_id)
    if state:
        params["state"] = state
    if order_by:
        params["orderBy"] = order_by
    if order_direction:
        params["orderDirection"] = order_direction

    return self._get("/executions", params=params, account_id_override=account_id_override)


def get_date_range_analytics(
    self: Client,
    start_date: str,
    start_time: str,
    account_id: Optional[int] = None,
    account_id_override: Optional[str] = None,
) -> dict:
    """
    Get execution counts grouped by minute buckets for a date range.

    Args:
        start_date: Start date for analytics (YYYY-MM-DD format)
        start_time: Start time for analytics (HH:MM:SS or HH:MM format)
        account_id: Account ID (optional, can also use account_id_override)
        account_id_override: Optional account ID override
    """
    params = {
        "startDate": start_date,
        "startTime": start_time,
    }
    
    account_id_header = account_id_override or (str(account_id) if account_id else None)
    
    return self._get("/executions/analytics", params=params, account_id_override=account_id_header)


def get_execution_totals(
    self: Client,
    account_id: int,
    account_id_override: Optional[str] = None,
) -> dict:
    """
    Get total counts of scheduled, success, and failed executions for an account.

    Args:
        account_id: Account ID
        account_id_override: Optional account ID override
    """
    account_id_header = account_id_override or str(account_id)
    return self._get("/executions/totals", params=None, account_id_override=account_id_header)


def cleanup_old_execution_logs(
    self: Client,
    account_id: str,
    retention_months: int,
    account_id_override: Optional[str] = None,
) -> dict:
    """
    Clean up old execution logs for an account based on retention period.

    Args:
        account_id: Account ID for which to cleanup logs
        retention_months: Number of months to retain logs (logs older than this will be deleted)
        account_id_override: Optional account ID override
    """
    account_id_header = account_id_override or account_id
    body = {
        "accountId": account_id,
        "retentionMonths": retention_months,
    }
    return self._post("/executions/cleanup-old-logs", body=body, account_id_override=account_id_header)


# Attach methods to Client class
Client.list_executions = list_executions
Client.get_date_range_analytics = get_date_range_analytics
Client.get_execution_totals = get_execution_totals
Client.cleanup_old_execution_logs = cleanup_old_execution_logs

