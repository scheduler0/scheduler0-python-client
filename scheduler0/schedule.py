"""
Schedule-from-prompt method for the Scheduler0 client (POST /ai/schedule).
"""

from typing import Any, Dict, Optional, Union

from .client import Client
from .prompt import _parse_classification
from .types import ScheduleResult, SchedulePromptRequest


def schedule_from_prompt(
    self: Client,
    body: Union[SchedulePromptRequest, Dict[str, Any]],
    account_id_override: Optional[str] = None,
) -> ScheduleResult:
    """
    Turn a natural-language prompt into actually-scheduled jobs.

    The server runs the prompt pipeline (intent guardrail + generation), resolves or
    creates a project, picks the executor whose description/tags best match the prompt
    (or uses a pinned executor_id / the account's only executor), and creates the jobs
    synchronously.

    Note: this endpoint consumes 1 prompt-request credit and requires valid credentials
    plus an account ID. A prompt rejected by the intent guardrail raises requests.HTTPError
    (HTTP 422); a prompt with no schedulable jobs or no matching executor raises
    requests.HTTPError (HTTP 409).

    Args:
        body: SchedulePromptRequest (or an equivalent dict).
        account_id_override: Optional account ID override.

    Returns:
        ScheduleResult with the classification, project (+ created flag), executor
        (+ match strategy/reason), created jobs, and the provider/model used.
    """
    response = self._request(
        "POST", "/ai/schedule", body=body, params=None, account_id_override=account_id_override
    )
    data: Dict[str, Any] = response.json().get("data", {}) or {}

    return ScheduleResult(
        classification=_parse_classification(data.get("classification")),
        project=data.get("project"),
        project_created=bool(data.get("projectCreated", False)),
        executor=data.get("executor"),
        executor_matched_by=data.get("executorMatchedBy", ""),
        executor_match_reason=data.get("executorMatchReason"),
        jobs=data.get("jobs", []) or [],
        provider=data.get("provider"),
        model=data.get("model"),
    )


# Attach method to Client class
Client.schedule_from_prompt = schedule_from_prompt
