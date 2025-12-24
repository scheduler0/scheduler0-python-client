"""
Tests for AI prompt methods.
"""

import pytest
from unittest.mock import patch, Mock
from scheduler0.types import PromptJobRequest


class TestPrompt:
    """Test AI prompt methods."""

    @patch('scheduler0.client.Client._request')
    def test_create_job_from_prompt(self, mock_request, client):
        """Test creating jobs from AI prompt."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "kind": "email",
                "cronExpression": "0 9 * * 1",
                "timezone": "America/New_York",
                "recipients": ["team@example.com"],
            },
        ]
        mock_request.return_value = mock_response

        body = PromptJobRequest(
            prompt="Send weekly reports every Monday at 9 AM",
            purposes=["reporting"],
            timezone="America/New_York",
        )
        result = client.create_job_from_prompt(body)
        assert len(result) == 1
        assert result[0]["kind"] == "email"
        assert result[0]["cronExpression"] == "0 9 * * 1"
        mock_request.assert_called_once_with(
            "POST", "/prompt", body=body, params=None, account_id_override=None
        )

    @patch('scheduler0.client.Client._request')
    def test_create_job_from_prompt_with_metadata(self, mock_request, client):
        """Test creating jobs from AI prompt with full metadata."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "kind": "notification",
                "cronExpression": "0 0 * * *",
                "recipients": ["user@example.com"],
                "channels": ["email"],
            },
        ]
        mock_request.return_value = mock_response

        body = PromptJobRequest(
            prompt="Send daily notifications",
            purposes=["communication"],
            events=["daily"],
            recipients=["user@example.com"],
            channels=["email"],
        )
        result = client.create_job_from_prompt(body)
        assert len(result) == 1
        assert result[0]["channels"] == ["email"]

