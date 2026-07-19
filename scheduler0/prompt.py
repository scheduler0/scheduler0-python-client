"""
AI-powered job creation methods for Scheduler0 client.
"""

from typing import Optional, Any, Dict, List
from .client import Client
from .types import (
    PromptJobRequest,
    PromptJobResponse,
    PromptProviderResult,
    IntentClassification,
    PromptResult,
    PromptRequest,
    PromptRequestsResult,
    ClassifyPromptRequest,
)


def _parse_classification(raw: Optional[Dict[str, Any]]) -> Optional[IntentClassification]:
    if raw is None:
        return None

    return IntentClassification(
        text=raw.get("text", ""),
        decision=raw.get("decision", ""),
        reason=raw.get("reason", ""),
    )


def create_job_from_prompt(
    self: Client,
    body: PromptJobRequest,
    account_id_override: Optional[str] = None,
) -> PromptResult:
    """
    Create job configurations from natural language prompts using AI.

    Note: This endpoint requires credits and validates credentials.
    1 credit per prompt execution.

    Args:
        body: Prompt job request with prompt and optional metadata
        account_id_override: Optional account ID override

    Returns:
        PromptResult with providers (list of PromptProviderResult) and an optional
        IntentClassification containing the full classifier output.
    """
    response = self._request("POST", "/ai/prompt", body=body, params=None, account_id_override=account_id_override)
    data: Dict[str, Any] = response.json()["data"]

    providers = []
    for pr in data.get("providers", []):
        jobs = [
            PromptJobResponse(
                kind=j.get("kind"),
                purpose=j.get("purpose"),
                subject=j.get("subject"),
                next_run_at=j.get("nextRunAt"),
                recurrence=j.get("recurrence"),
                event=j.get("event"),
                delivery=j.get("delivery"),
                cron_expression=j.get("cronExpression"),
                channel=j.get("channel"),
                recipients=j.get("recipients"),
                start_date=j.get("startDate"),
                end_date=j.get("endDate"),
                timezone=j.get("timezone"),
                metadata=j.get("metadata"),
            )
            for j in (pr.get("jobs") or [])
        ]
        providers.append(PromptProviderResult(
            provider=pr.get("provider", ""),
            model=pr.get("model", ""),
            jobs=jobs,
            input_tokens=pr.get("inputTokens", 0),
            output_tokens=pr.get("outputTokens", 0),
            total_tokens=pr.get("totalTokens", 0),
            duration_ms=pr.get("durationMs", 0),
        ))

    classification = _parse_classification(data.get("classification"))
    return PromptResult(providers=providers, classification=classification)


def classify_prompt(
    self: Client,
    body: ClassifyPromptRequest,
    account_id_override: Optional[str] = None,
) -> IntentClassification:
    """
    Run only the intent classifier against the prompt — no AI model is invoked
    and no credits are consumed. Raises an exception when the classifier is not
    configured on the server (503 Service Unavailable).

    Args:
        body: ClassifyPromptRequest with the prompt text
        account_id_override: Optional account ID override

    Returns:
        IntentClassification with the full classifier output.
    """
    response = self._request("POST", "/ai/prompt/classify", body=body, params=None, account_id_override=account_id_override)
    data: Dict[str, Any] = response.json()["data"]
    return _parse_classification(data.get("classification")) or IntentClassification()


def list_prompt_requests(
    self: Client,
    limit: int = 25,
    offset: int = 0,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    order: Optional[str] = None,
    account_id_override: Optional[str] = None,
) -> PromptRequestsResult:
    """
    Retrieve the account's AI prompt-request log with optional filters and pagination.

    Args:
        limit: Maximum number of items to return
        offset: Number of items to skip
        provider: Filter by AI provider (optional)
        model: Filter by model (optional)
        status: Filter by status - e.g. "success", "failed", "skipped_intent" (optional)
        search: Full-text search over the prompt (optional)
        start: Start date for filtering (RFC3339, optional)
        end: End date for filtering (RFC3339, optional)
        order: Sort direction - "ASC" or "DESC" (optional)
        account_id_override: Optional account ID override

    Returns:
        PromptRequestsResult with the list of PromptRequest entries plus pagination totals.
    """
    params: Dict[str, Any] = {"limit": str(limit), "offset": str(offset)}
    if provider:
        params["provider"] = provider
    if model:
        params["model"] = model
    if status:
        params["status"] = status
    if search:
        params["search"] = search
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    if order:
        params["order"] = order

    response = self._get("/ai/prompt-requests", params=params, account_id_override=account_id_override)
    data: Dict[str, Any] = response.get("data", {}) or {}

    requests = [
        PromptRequest(
            id=r.get("id", 0),
            account_id=r.get("account_id", 0),
            prompt=r.get("prompt", ""),
            provider=r.get("provider", ""),
            model=r.get("model", ""),
            output=r.get("output", ""),
            input_tokens=r.get("input_tokens", 0),
            output_tokens=r.get("output_tokens", 0),
            total_tokens=r.get("total_tokens", 0),
            duration_ms=r.get("duration_ms", 0),
            estimated_cost_usd=r.get("estimated_cost_usd", 0.0),
            status=r.get("status", ""),
            error=r.get("error"),
            date_created=r.get("date_created", ""),
        )
        for r in (data.get("requests") or [])
    ]

    return PromptRequestsResult(
        requests=requests,
        total=data.get("total", 0),
        limit=data.get("limit", 0),
        offset=data.get("offset", 0),
    )


# Attach methods to Client class
Client.create_job_from_prompt = create_job_from_prompt
Client.classify_prompt = classify_prompt
Client.list_prompt_requests = list_prompt_requests
