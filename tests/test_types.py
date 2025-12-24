"""
Tests for type definitions.
"""

import pytest
from scheduler0.types import (
    AccountCreateRequestBody,
    JobRequestBody,
    ProjectRequestBody,
    CredentialCreateRequestBody,
    ExecutorRequestBody,
    PromptJobRequest,
)


class TestTypes:
    """Test type definitions."""

    def test_account_create_request_body(self):
        """Test AccountCreateRequestBody."""
        body = AccountCreateRequestBody(name="Test Account")
        assert body.name == "Test Account"
        assert body.account_id is None

    def test_job_request_body(self):
        """Test JobRequestBody."""
        body = JobRequestBody(
            project_id=123,
            timezone="UTC",
            created_by="user@example.com",
        )
        assert body.project_id == 123
        assert body.timezone == "UTC"
        assert body.created_by == "user@example.com"
        assert body.account_id is None

    def test_project_request_body(self):
        """Test ProjectRequestBody."""
        body = ProjectRequestBody(
            name="Test Project",
            description="Description",
            created_by="user@example.com",
        )
        assert body.name == "Test Project"
        assert body.description == "Description"

    def test_credential_create_request_body(self):
        """Test CredentialCreateRequestBody."""
        body = CredentialCreateRequestBody(created_by="user@example.com")
        assert body.created_by == "user@example.com"
        assert body.archived is False

    def test_executor_request_body(self):
        """Test ExecutorRequestBody."""
        body = ExecutorRequestBody(
            name="webhook-executor",
            type="webhook_url",
            created_by="user@example.com",
        )
        assert body.name == "webhook-executor"
        assert body.type == "webhook_url"

    def test_prompt_job_request(self):
        """Test PromptJobRequest."""
        body = PromptJobRequest(
            prompt="Send weekly reports",
            purposes=["reporting"],
            recipients=["team@example.com"],
        )
        assert body.prompt == "Send weekly reports"
        assert body.purposes == ["reporting"]
        assert body.recipients == ["team@example.com"]

