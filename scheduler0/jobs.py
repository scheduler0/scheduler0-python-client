"""
Job management methods for Scheduler0 client.
"""

from typing import Optional, List
from .client import Client
from .types import JobRequestBody, JobUpdateRequestBody, JobDeleteRequestBody


def list_jobs(
    self: Client,
    project_id: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    order_by: Optional[str] = None,
    order_by_direction: Optional[str] = None,
    account_id_override: Optional[str] = None,
) -> dict:
    """List jobs with pagination and ordering."""
    params = {
        "limit": str(limit),
        "offset": str(offset),
    }
    if project_id:
        params["projectId"] = project_id
    if order_by:
        params["orderBy"] = order_by
    if order_by_direction:
        params["orderByDirection"] = order_by_direction

    return self._get("/jobs", params=params, account_id_override=account_id_override)


def create_job(
    self: Client,
    body: JobRequestBody,
    account_id_override: Optional[str] = None,
) -> dict:
    """Create a single job (convenience method that wraps batch creation)."""
    return self.batch_create_jobs([body], account_id_override=account_id_override)


def batch_create_jobs(
    self: Client,
    jobs: List[JobRequestBody],
    account_id_override: Optional[str] = None,
) -> dict:
    """Create multiple jobs in a single request."""
    return self._post("/jobs", jobs, account_id_override=account_id_override)


def get_job(
    self: Client,
    job_id: str,
    account_id_override: Optional[str] = None,
) -> dict:
    """Get a specific job."""
    return self._get(f"/jobs/{job_id}", params=None, account_id_override=account_id_override)


def update_job(
    self: Client,
    job_id: str,
    body: JobUpdateRequestBody,
    account_id_override: Optional[str] = None,
) -> dict:
    """Update a job."""
    return self._put(f"/jobs/{job_id}", body, account_id_override=account_id_override)


def delete_job(
    self: Client,
    job_id: str,
    body: JobDeleteRequestBody,
    account_id_override: Optional[str] = None,
) -> None:
    """Delete a job."""
    self._delete(f"/jobs/{job_id}", body, account_id_override=account_id_override)


# Attach methods to Client class
Client.list_jobs = list_jobs
Client.create_job = create_job
Client.batch_create_jobs = batch_create_jobs
Client.get_job = get_job
Client.update_job = update_job
Client.delete_job = delete_job

