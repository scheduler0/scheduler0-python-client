"""
Tests for type definitions.
"""

import pytest
from scheduler0.types import (
    AccountCreateRequestBody,
    JobRequestBody,
    ProjectRequestBody,
    Credential,
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
        body = CredentialCreateRequestBody(
            created_by="user@example.com",
            scopes=["read", "write"],
        )
        assert body.created_by == "user@example.com"
        assert body.archived is False
        assert body.scopes == ["read", "write"]

    def test_credential_create_request_body_defaults(self):
        """Defaults should produce an empty scope list rather than None so the
        client sends an explicit (and easily inspected) scopes array."""
        body = CredentialCreateRequestBody(created_by="user@example.com")
        assert body.scopes == []

    def test_credential_includes_expiry_and_scopes(self):
        """Credential responses must round-trip the expiry and scope fields.

        The encrypted ``api_secret`` is never returned by the API, so it is not a
        field on the type. ``plaintext_secret`` is returned only on creation.
        """
        cred = Credential(
            id=1,
            account_id=2,
            archived=False,
            api_key="key",
            date_created="2025-01-01T00:00:00Z",
            expires_at="2025-04-01T00:00:00Z",
            scopes=["read", "write", "execute"],
            plaintext_secret="plaintext-once",
        )
        assert cred.expires_at == "2025-04-01T00:00:00Z"
        assert cred.scopes == ["read", "write", "execute"]
        assert cred.plaintext_secret == "plaintext-once"

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

