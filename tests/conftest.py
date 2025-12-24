"""
Pytest fixtures for Scheduler0 Python client tests.
"""

import pytest
from unittest.mock import Mock, patch
from scheduler0 import Client


@pytest.fixture
def base_url():
    """Base URL for testing."""
    return "http://localhost:7070"


@pytest.fixture
def api_key():
    """API key for testing."""
    return "test-api-key"


@pytest.fixture
def api_secret():
    """API secret for testing."""
    return "test-api-secret"


@pytest.fixture
def account_id():
    """Account ID for testing."""
    return "123"


@pytest.fixture
def client(base_url, api_key, api_secret, account_id):
    """Create a test client with API key authentication."""
    return Client(
        base_url=base_url,
        version="v1",
        api_key=api_key,
        api_secret=api_secret,
        account_id=account_id,
    )


@pytest.fixture
def basic_auth_client(base_url):
    """Create a test client with basic authentication."""
    return Client(
        base_url=base_url,
        version="v1",
        username="testuser",
        password="testpass",
    )


@pytest.fixture
def mock_response():
    """Create a mock response object."""
    def _create(status_code=200, json_data=None, text=""):
        response = Mock()
        response.status_code = status_code
        response.json.return_value = json_data or {}
        response.text = text
        return response
    return _create

