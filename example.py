"""
Example usage of the Scheduler0 Python client.

Set SCHEDULER0_API_KEY, SCHEDULER0_API_SECRET and SCHEDULER0_ACCOUNT_ID, then run:

    python example.py
"""

import os

import requests

from scheduler0 import Client
from scheduler0.types import (
    ExecutorRequestBody,
    JobRequestBody,
    ProjectRequestBody,
)


def main():
    client = Client(
        base_url=os.environ.get("SCHEDULER0_BASE_URL", "https://api.scheduler0.com"),
        api_key=os.environ["SCHEDULER0_API_KEY"],
        api_secret=os.environ["SCHEDULER0_API_SECRET"],
        account_id=os.environ["SCHEDULER0_ACCOUNT_ID"],
    )

    # GET /healthcheck (no auth required)
    health = client.healthcheck()
    print("leader:", health["data"]["leaderAddress"])

    try:
        # POST /projects -> 201
        project = client.create_project(ProjectRequestBody(
            name="Example Project",
            description="Created by example.py",
            created_by="example@example.com",
        ))["data"]
        print("project id:", project["id"])

        # POST /executors -> 201 (webhook_url needs webhook_url + webhook_method)
        executor = client.create_executor(ExecutorRequestBody(
            name="example-webhook",
            type="webhook_url",
            webhook_url="https://example.com/webhook",
            webhook_method="POST",
            created_by="example@example.com",
        ))["data"]
        print("executor id:", executor["id"])

        # POST /jobs -> 202 with a request id; poll GET /async-tasks/{id}
        accepted = client.create_job(JobRequestBody(
            project_id=project["id"],
            timezone="UTC",
            created_by="example@example.com",
            executor_id=executor["id"],
            spec="0 * * * * *",  # every minute
            data='{"hello": "world"}',
        ))
        request_id = accepted["data"]
        task = client.get_async_task(request_id)["data"]
        print("async task state:", task["state"])  # 2 = success, 3 = failed

        # GET /jobs?projectId=...
        page = client.list_jobs(project_id=str(project["id"]), limit=10, offset=0)
        print("jobs in project:", page["data"]["total"])
    except requests.HTTPError as e:
        print("API error", e.response.status_code, e.response.json().get("data"))


if __name__ == "__main__":
    main()
