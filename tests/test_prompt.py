"""
Tests for AI prompt methods.
"""

import pytest
from unittest.mock import patch, Mock
from scheduler0.types import (
    PromptJobRequest,
    PromptResult,
    IntentClassification,
    ClassifyPromptRequest,
)


class TestPrompt:
    """Test AI prompt methods."""

    @patch('scheduler0.client.Client._request')
    def test_create_job_from_prompt(self, mock_request, client):
        """Test creating jobs from AI prompt.

        The API wraps the result in the standard ``{success, data}`` envelope,
        where ``data`` is a PromptResult with ``providers`` and optional ``classification``.
        """
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "data": {
                "providers": [
                    {
                        "provider": "openai",
                        "model": "gpt-4.1-mini",
                        "jobs": [
                            {
                                "kind": "REMINDER",
                                "cronExpression": "0 9 * * 1",
                                "timezone": "America/New_York",
                                "recipients": ["team@example.com"],
                            },
                        ],
                        "inputTokens": 120,
                        "outputTokens": 80,
                        "totalTokens": 200,
                        "durationMs": 1500,
                    },
                ],
                "classification": {
                    "text": "Send weekly reports every Monday at 9 AM",
                    "decision": "allow",
                    "reason": "request_with_temporal_signal",
                },
            },
        }
        mock_request.return_value = mock_response

        body = PromptJobRequest(
            prompt="Send weekly reports every Monday at 9 AM",
            purposes=["reporting"],
            timezone="America/New_York",
        )
        result = client.create_job_from_prompt(body)
        assert isinstance(result, PromptResult)
        assert len(result.providers) == 1
        assert result.providers[0].provider == "openai"
        assert result.providers[0].jobs[0].cron_expression == "0 9 * * 1"
        assert result.classification is not None
        assert result.classification.decision == "allow"
        assert result.classification.reason == "request_with_temporal_signal"
        mock_request.assert_called_once_with(
            "POST", "/ai/prompt", body=body, params=None, account_id_override=None
        )

    @patch('scheduler0.client.Client._request')
    def test_create_job_from_prompt_with_metadata(self, mock_request, client):
        """Test creating jobs from AI prompt without classification (classifier disabled)."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "data": {
                "providers": [
                    {
                        "provider": "anthropic",
                        "model": "claude-sonnet-4-5",
                        "jobs": [
                            {
                                "kind": "DIGEST",
                                "cronExpression": "0 0 * * *",
                                "recipients": ["user@example.com"],
                                "channel": "email",
                            },
                        ],
                        "inputTokens": 90,
                        "outputTokens": 60,
                        "totalTokens": 150,
                        "durationMs": 1200,
                    },
                ],
            },
        }
        mock_request.return_value = mock_response

        body = PromptJobRequest(
            prompt="Send daily notifications",
            purposes=["communication"],
            events=["daily"],
            recipients=["user@example.com"],
            channels=["email"],
        )
        result = client.create_job_from_prompt(body)
        assert isinstance(result, PromptResult)
        assert len(result.providers) == 1
        assert result.providers[0].provider == "anthropic"
        assert result.providers[0].jobs[0].channel == "email"
        assert result.classification is None

    @patch('scheduler0.client.Client._request')
    def test_classify_prompt(self, mock_request, client):
        """Test classify_prompt returns a fully-populated IntentClassification."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "data": {
                "classification": {
                    "text": "What is Kubernetes?",
                    "decision": "reject",
                    "reason": "informational_question_not_schedule_request",
                },
            },
        }
        mock_request.return_value = mock_response

        body = ClassifyPromptRequest(prompt="What is Kubernetes?")
        result = client.classify_prompt(body)
        assert isinstance(result, IntentClassification)
        assert result.decision == "reject"
        assert result.reason == "informational_question_not_schedule_request"
        mock_request.assert_called_once_with(
            "POST", "/ai/prompt/classify", body=body, params=None, account_id_override=None
        )
