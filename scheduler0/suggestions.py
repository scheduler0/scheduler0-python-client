"""
Conversation suggestions analysis for the Scheduler0 client.
"""

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Optional, Union

import requests

from .client import Client
from .types import (
    AnalyzeSuggestionsRequest,
    AnalyzeSuggestionsResult,
    SendTimeSuggestionsRequest,
    SendTimeSuggestionsResult,
)


def _strip_none(obj: Any) -> Any:
    """Recursively drop keys/items whose value is None."""
    if isinstance(obj, dict):
        return {k: _strip_none(v) for k, v in obj.items() if v is not None}
    if isinstance(obj, list):
        return [_strip_none(v) for v in obj]
    return obj


def _to_payload(body: Any) -> Dict[str, Any]:
    """Build the snake_case JSON payload for a suggestions endpoint.

    The suggestions APIs use snake_case field names, so this bypasses the
    client's default camelCase body serializer. ``dataclasses.asdict`` preserves
    the snake_case dataclass field names (and a bare-string speaker stays a string).
    """
    if is_dataclass(body):
        raw = asdict(body)
    elif isinstance(body, dict):
        raw = body
    else:
        raise TypeError("body must be a suggestions request dataclass or a dict")
    return _strip_none(raw)


def analyze_suggestions(
    self: Client,
    body: Union[AnalyzeSuggestionsRequest, Dict[str, Any]],
    account_id_override: Optional[str] = None,
) -> AnalyzeSuggestionsResult:
    """
    Analyze a conversation and return structured, explainable suggestions
    (commitments, requests, deadlines, follow-ups, etc.) plus the obligations
    they map to.

    English only: a non-``en*`` locale in ``options`` is rejected by the API with
    UNSUPPORTED_LOCALE (400).

    Args:
        body: AnalyzeSuggestionsRequest (or an equivalent snake_case dict).
        account_id_override: Optional account ID override.

    Returns:
        AnalyzeSuggestionsResult with suggestions, obligations, warnings, and
        engine metadata.
    """
    payload = _to_payload(body)
    account_id = self._resolve_account_id(body, account_id_override)
    headers = self._prepare_headers(account_id)
    url = self._build_url("/suggestions/analyze")

    response = self.session.request(
        method="POST",
        url=url,
        headers=headers,
        json=payload,
        auth=(self.username, self.password) if self.username and self.password else None,
    )

    if response.status_code >= 400:
        error_msg = f"API error: {response.status_code}"
        try:
            error_body = response.json()
            if isinstance(error_body, dict) and "message" in error_body:
                error_msg = error_body["message"]
            else:
                error_msg = response.text
        except (ValueError, KeyError):
            error_msg = response.text
        raise requests.HTTPError(f"{error_msg} - {response.text}", response=response)

    data: Dict[str, Any] = response.json().get("data", {}) or {}
    return AnalyzeSuggestionsResult(
        request_id=data.get("request_id"),
        conversation_id=data.get("conversation_id"),
        analyzed_at=data.get("analyzed_at"),
        suggestions=data.get("suggestions", []) or [],
        obligations=data.get("obligations", []) or [],
        warnings=data.get("warnings", []) or [],
        engine=data.get("engine"),
    )


def send_time_suggestions(
    self: Client,
    body: Union[SendTimeSuggestionsRequest, Dict[str, Any]],
    account_id_override: Optional[str] = None,
) -> SendTimeSuggestionsResult:
    """
    Recommend suitable future send times for a message given sender/recipient
    time zones, working hours, quiet hours, weekends, priority, and coverage
    rules. The engine is deterministic and does not send the message or create
    a job.

    Args:
        body: SendTimeSuggestionsRequest (or an equivalent snake_case dict).
        account_id_override: Optional account ID override.

    Returns:
        SendTimeSuggestionsResult with ranked suggestions, search metadata,
        optional send_now evaluation, and warnings.
    """
    payload = _to_payload(body)
    account_id = self._resolve_account_id(body, account_id_override)
    headers = self._prepare_headers(account_id)
    url = self._build_url("/send-time-suggestions")

    response = self.session.request(
        method="POST",
        url=url,
        headers=headers,
        json=payload,
        auth=(self.username, self.password) if self.username and self.password else None,
    )

    if response.status_code >= 400:
        error_msg = f"API error: {response.status_code}"
        try:
            error_body = response.json()
            if isinstance(error_body, dict) and "message" in error_body:
                error_msg = error_body["message"]
            else:
                error_msg = response.text
        except (ValueError, KeyError):
            error_msg = response.text
        raise requests.HTTPError(f"{error_msg} - {response.text}", response=response)

    data: Dict[str, Any] = response.json().get("data", {}) or {}
    return SendTimeSuggestionsResult(
        request_id=data.get("request_id"),
        reference_time=data.get("reference_time"),
        policy=data.get("policy"),
        engine=data.get("engine"),
        suggestions=data.get("suggestions", []) or [],
        search=data.get("search"),
        rejected_summary=data.get("rejected_summary"),
        no_suggestion=data.get("no_suggestion"),
        send_now=data.get("send_now"),
        warnings=data.get("warnings", []) or [],
        metadata=data.get("metadata"),
    )


# Attach methods to Client class
Client.analyze_suggestions = analyze_suggestions
Client.send_time_suggestions = send_time_suggestions
