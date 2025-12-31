"""
Project management methods for Scheduler0 client.
"""

from typing import Optional
from .client import Client
from .types import ProjectRequestBody, ProjectUpdateRequestBody, ProjectDeleteRequestBody


def list_projects(
    self: Client,
    limit: int = 10,
    offset: int = 0,
    order_by: Optional[str] = None,
    order_by_direction: Optional[str] = None,
    account_id_override: Optional[str] = None,
) -> dict:
    """List projects with pagination and ordering."""
    params = {
        "limit": str(limit),
        "offset": str(offset),
    }
    if order_by:
        params["orderBy"] = order_by
    if order_by_direction:
        params["orderByDirection"] = order_by_direction

    return self._get("/projects", params=params, account_id_override=account_id_override)


def create_project(
    self: Client,
    body: ProjectRequestBody,
    account_id_override: Optional[str] = None,
) -> dict:
    """Create a new project."""
    return self._post("/projects", body, account_id_override=account_id_override)


def get_project(
    self: Client,
    project_id: str,
    account_id_override: Optional[str] = None,
) -> dict:
    """Get a specific project."""
    return self._get(f"/projects/{project_id}", params=None, account_id_override=account_id_override)


def update_project(
    self: Client,
    project_id: str,
    body: ProjectUpdateRequestBody,
    account_id_override: Optional[str] = None,
) -> dict:
    """Update a project."""
    return self._put(f"/projects/{project_id}", body, account_id_override=account_id_override)


def delete_project(
    self: Client,
    project_id: str,
    body: ProjectDeleteRequestBody,
    account_id_override: Optional[str] = None,
) -> None:
    """Delete a project."""
    self._delete(f"/projects/{project_id}", body, account_id_override=account_id_override)


# Attach methods to Client class
Client.list_projects = list_projects
Client.create_project = create_project
Client.get_project = get_project
Client.update_project = update_project
Client.delete_project = delete_project

