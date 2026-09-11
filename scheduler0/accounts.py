"""
Account management methods for Scheduler0 client.
"""

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Optional

import requests

from .client import Client
from .types import AccountCreateRequestBody, AccountUpdateRequestBody, AccountAISettings, ActiveModel, FeatureRequest


def _ai_settings_payload(body: Any) -> Dict[str, Any]:
    """Build the snake_case JSON payload for /ai/settings.

    The AI settings API uses snake_case field names (see models.AccountAISettings),
    so this bypasses the client's default camelCase body serializer -- same pattern
    as suggestions._to_payload for /ai/suggestions/*.
    """
    if is_dataclass(body):
        raw = asdict(body)
    elif isinstance(body, dict):
        raw = body
    else:
        raise TypeError("body must be an AccountAISettings dataclass or a dict")
    return {k: v for k, v in raw.items() if v is not None and k != "account_id"}


def create_account(self: Client, body: AccountCreateRequestBody) -> dict:
    """Create a new account."""
    return self._post("/accounts", body, account_id_override=None)


def get_account(self: Client, account_id: str) -> dict:
    """Get account details by ID."""
    return self._get(f"/accounts/{account_id}", params=None, account_id_override=account_id)


def update_account(self: Client, account_id: str, body: AccountUpdateRequestBody) -> dict:
    """Update an account (e.g. rename)."""
    return self._put(f"/accounts/{account_id}", body, account_id_override=account_id)


def add_feature_to_account(self: Client, account_id: str, body: FeatureRequest) -> dict:
    """Add a feature to an account."""
    return self._put(f"/accounts/{account_id}/feature", body, account_id_override=account_id)


def remove_feature_from_account(self: Client, account_id: str, body: FeatureRequest) -> None:
    """Remove a feature from an account."""
    self._delete(f"/accounts/{account_id}/feature", body, account_id_override=account_id)


def add_all_features_to_account(self: Client, account_id: str) -> None:
    """Add all features to an account."""
    self._request("PUT", f"/accounts/{account_id}/features/all", None, params=None, account_id_override=account_id)


def remove_all_features_from_account(self: Client, account_id: str) -> None:
    """Remove all features from an account."""
    self._request("DELETE", f"/accounts/{account_id}/features/all", None, params=None, account_id_override=account_id)


def get_account_execution_count(self: Client, account_id: str) -> dict:
    """Get execution count for an account."""
    return self._get(f"/accounts/{account_id}/execution-count", params=None, account_id_override=account_id)


def increase_account_execution_count(self: Client, account_id: str, count: int) -> dict:
    """Increase execution count for an account."""
    body = {"count": count}
    return self._put(f"/accounts/{account_id}/execution-count", body, account_id_override=account_id)


def get_ai_usage(self: Client, account_id: str) -> dict:
    """Get the account's log-derived AI request usage for the current period.

    Returns prompt and classify limits (feature-derived), the number of successful
    requests used, the remaining allowance, the summed estimated prompt cost in USD, and
    the period boundary. This is the single source of truth for AI credit usage and
    replaces the removed classify-count/prompt-count endpoints.
    """
    return self._get(f"/accounts/{account_id}/ai/usage", params=None, account_id_override=account_id)


def get_account_tokens(self: Client, account_id: str) -> dict:
    """Get the current token balance for an account."""
    return self._get(f"/accounts/{account_id}/tokens", params=None, account_id_override=account_id)


def add_account_tokens(self: Client, account_id: str, amount: int) -> dict:
    """Add tokens to an account's balance."""
    body = {"amount": amount}
    return self._put(f"/accounts/{account_id}/tokens/add", body, account_id_override=account_id)


def get_account_ai_settings(self: Client, account_id: str) -> dict:
    """Get the AI provider settings for an account."""
    return self._get("/ai/settings", params=None, account_id_override=account_id)


def upsert_account_ai_settings(self: Client, account_id: str, body: AccountAISettings) -> dict:
    """Create or update the AI provider settings for an account.

    Pass an ``active_models`` list to configure the primary model and
    optional fallbacks.  The first entry is primary; subsequent entries
    are tried in order if the primary fails.

    Example::

        from scheduler0 import Client, AccountAISettings, ActiveModel

        client = Client(...)
        client.upsert_account_ai_settings(
            account_id="123",
            body=AccountAISettings(
                active_models=[
                    ActiveModel(provider="openai", model="gpt-4.1-mini"),
                    ActiveModel(provider="anthropic", model="claude-sonnet-4-5"),
                ],
                openai_api_key="sk-...",
                anthropic_api_key="sk-ant-...",
            ),
        )
    """
    payload = _ai_settings_payload(body)
    resolved_account_id = self._resolve_account_id(None, account_id)
    headers = self._prepare_headers(resolved_account_id)
    url = self._build_url("/ai/settings")

    response = self.session.request(
        method="PUT",
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

    return response.json()


def get_ai_models(self: Client) -> dict:
    """Retrieve the per-provider approved model catalog.

    Returns a dict with keys ``success`` and ``data``, where ``data`` maps
    provider names to lists of approved model dicts (``id``, ``display_name``,
    ``default``).

    Example::

        catalog = client.get_ai_models()
        openai_models = catalog["data"]["openai"]
        # [{"id": "gpt-4.1-mini", "display_name": "GPT-4.1 Mini", "default": True}, ...]
    """
    return self._get("/ai/models", params=None, account_id_override=None)


# Attach methods to Client class
Client.create_account = create_account
Client.get_account = get_account
Client.update_account = update_account
Client.add_feature_to_account = add_feature_to_account
Client.remove_feature_from_account = remove_feature_from_account
Client.add_all_features_to_account = add_all_features_to_account
Client.remove_all_features_from_account = remove_all_features_from_account
Client.get_account_execution_count = get_account_execution_count
Client.increase_account_execution_count = increase_account_execution_count
Client.get_ai_usage = get_ai_usage
Client.get_account_tokens = get_account_tokens
Client.add_account_tokens = add_account_tokens
Client.get_account_ai_settings = get_account_ai_settings
Client.upsert_account_ai_settings = upsert_account_ai_settings
Client.get_ai_models = get_ai_models

