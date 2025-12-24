"""
Example usage of the Scheduler0 Python client.

This file demonstrates basic usage patterns.
"""

from scheduler0 import NewAPIClientWithAccount
from scheduler0.types import (
    AccountCreateRequestBody,
    JobRequestBody,
    ProjectRequestBody,
    CredentialCreateRequestBody,
)


def main():
    # Initialize client
    client = NewAPIClientWithAccount(
        base_url="http://localhost:7070",
        version="v1",
        api_key="your-api-key",
        api_secret="your-api-secret",
        account_id="123",
    )

    # Example: Health check (no auth required)
    try:
        health = client.healthcheck()
        print(f"Cluster health: {health}")
    except Exception as e:
        print(f"Health check failed: {e}")

    # Example: Create a project
    try:
        project = ProjectRequestBody(
            name="Example Project",
            description="An example project",
            created_by="user@example.com",
        )
        result = client.create_project(project)
        print(f"Created project: {result}")
    except Exception as e:
        print(f"Failed to create project: {e}")

    # Example: List jobs
    try:
        jobs = client.list_jobs(limit=10, offset=0)
        print(f"Jobs: {jobs}")
    except Exception as e:
        print(f"Failed to list jobs: {e}")


if __name__ == "__main__":
    main()

