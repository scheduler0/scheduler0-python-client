"""
Local executor methods for Scheduler0 client.

Local executors run jobs as shell commands on a machine you control. The
scheduler0-cli process uses the pull/report endpoints; you normally only call
``register_local_executor`` directly.
"""

from typing import List, Optional, Union
from .client import Client
from .types import LocalExecutorRegisterRequest, LocalExecutionReport


def register_local_executor(
    self: Client,
    body: LocalExecutorRegisterRequest,
    account_id_override: Optional[str] = None,
) -> dict:
    """Register a new local executor. The server sets the executor type to "local".

    POST /local-executors
    """
    return self._post("/local-executors", body, account_id_override=account_id_override)


def pull_local_executor_jobs(
    self: Client,
    executor_id: Union[str, int],
    account_id_override: Optional[str] = None,
) -> dict:
    """Pull the active jobs assigned to a local executor.

    Each call also renews the executor's lease (heartbeat) and records a
    pull-log entry server-side.

    GET /local-executors/{id}/jobs
    """
    return self._get(
        f"/local-executors/{executor_id}/jobs",
        params=None,
        account_id_override=account_id_override,
    )


def report_local_executions(
    self: Client,
    executor_id: Union[str, int],
    reports: List[LocalExecutionReport],
    account_id_override: Optional[str] = None,
) -> dict:
    """Report a batch of local execution results.

    The events are committed via Raft and counted toward the account's
    execution quota.

    POST /local-executors/{id}/executions
    """
    return self._post(
        f"/local-executors/{executor_id}/executions",
        reports,
        account_id_override=account_id_override,
    )


# Attach methods to Client class
Client.register_local_executor = register_local_executor
Client.pull_local_executor_jobs = pull_local_executor_jobs
Client.report_local_executions = report_local_executions
