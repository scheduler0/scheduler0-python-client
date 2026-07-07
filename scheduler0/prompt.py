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
    response = self._request("POST", "/prompt", body=body, params=None, account_id_override=account_id_override)
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
    response = self._request("POST", "/prompt/classify", body=body, params=None, account_id_override=account_id_override)
    data: Dict[str, Any] = response.json()["data"]
    return _parse_classification(data.get("classification")) or IntentClassification()


# Attach methods to Client class
Client.create_job_from_prompt = create_job_from_prompt
Client.classify_prompt = classify_prompt
