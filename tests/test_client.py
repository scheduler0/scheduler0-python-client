"""
Tests for the core Client class.
"""

import pytest
import requests
from unittest.mock import Mock, patch, call
from scheduler0 import Client, NewClient, NewAPIClient, NewAPIClientWithAccount, NewBasicAuthClient
from scheduler0.types import JobRequestBody


class TestClientInitialization:
    """Test client initialization."""

    def test_client_init_with_api_key(self, base_url, api_key, api_secret, account_id):
        """Test client initialization with API key."""
        client = Client(
            base_url=base_url,
            version="v1",
            api_key=api_key,
            api_secret=api_secret,
            account_id=account_id,
        )
        assert client.base_url == base_url
        assert client.version == "v1"
        assert client.api_key == api_key
        assert client.api_secret == api_secret
        assert client.account_id == account_id

    def test_client_init_with_basic_auth(self, base_url):
        """Test client initialization with basic auth."""
        client = Client(
            base_url=base_url,
            version="v1",
            username="user",
            password="pass",
        )
        assert client.username == "user"
        assert client.password == "pass"
        assert client.api_key is None

    def test_client_init_invalid_url(self):
        """Test client initialization with invalid URL."""
        with pytest.raises(ValueError, match="base_url must include a scheme"):
            Client(base_url="localhost:7070", version="v1")

    def test_new_client_factory(self, base_url):
        """Test NewClient factory function."""
        client = NewClient(
            base_url=base_url,
            version="v1",
            api_key="key",
            api_secret="secret",
            account_id="123",
        )
        assert isinstance(client, Client)
        assert client.api_key == "key"

    def test_new_api_client_factory(self, base_url):
        """Test NewAPIClient factory function."""
        client = NewAPIClient(base_url, "v1", "key", "secret")
        assert isinstance(client, Client)
        assert client.api_key == "key"
        assert client.api_secret == "secret"

    def test_new_api_client_with_account_factory(self, base_url):
        """Test NewAPIClientWithAccount factory function."""
        client = NewAPIClientWithAccount(base_url, "v1", "key", "secret", "123")
        assert isinstance(client, Client)
        assert client.account_id == "123"

    def test_new_basic_auth_client_factory(self, base_url):
        """Test NewBasicAuthClient factory function."""
        client = NewBasicAuthClient(base_url, "v1", "user", "pass")
        assert isinstance(client, Client)
        assert client.username == "user"
        assert client.password == "pass"


class TestClientRequestBuilding:
    """Test request building and URL construction."""

    def test_build_url(self, client):
        """Test URL building."""
        url = client._build_url("/jobs")
        assert url == "http://localhost:7070/api/v1/jobs"

    def test_build_url_with_endpoint_slash(self, client):
        """Test URL building with leading slash in endpoint."""
        url = client._build_url("jobs")
        assert url == "http://localhost:7070/api/v1/jobs"

    def test_prepare_headers_with_api_key(self, client):
        """Test header preparation with API key."""
        headers = client._prepare_headers(account_id="123")
        assert headers["X-API-Key"] == "test-api-key"
        assert headers["X-Secret-Key"] == "test-api-secret"
        assert headers["X-Account-ID"] == "123"
        assert headers["Content-Type"] == "application/json"

    def test_prepare_headers_with_basic_auth(self, basic_auth_client):
        """Test header preparation with basic auth."""
        headers = basic_auth_client._prepare_headers()
        assert headers["X-Peer"] == "cmd"
        assert headers["Content-Type"] == "application/json"

    def test_resolve_account_id_from_override(self, client):
        """Test account ID resolution from override."""
        account_id = client._resolve_account_id(account_id_override="456")
        assert account_id == "456"

    def test_resolve_account_id_from_body(self, client):
        """Test account ID resolution from body."""
        body = Mock()
        body.account_id = "789"
        account_id = client._resolve_account_id(body=body)
        assert account_id == "789"

    def test_resolve_account_id_from_client_default(self, client):
        """Test account ID resolution from client default."""
        account_id = client._resolve_account_id()
        assert account_id == "123"


class TestClientSerialization:
    """Test request body serialization."""

    def test_serialize_dataclass(self, client):
        """Test serialization of dataclass."""
        from scheduler0.types import JobRequestBody
        body = JobRequestBody(
            project_id=123,
            timezone="UTC",
            created_by="test",
        )
        result = client._serialize_body(body)
        assert result["projectId"] == 123
        assert result["timezone"] == "UTC"
        assert result["createdBy"] == "test"
        assert "account_id" not in result

    def test_serialize_dict(self, client):
        """Test serialization of dictionary."""
        body = {"project_id": 123, "timezone": "UTC"}
        result = client._serialize_body(body)
        assert result["projectId"] == 123
        assert result["timezone"] == "UTC"

    def test_serialize_list(self, client):
        """Test serialization of list."""
        from scheduler0.types import JobRequestBody
        jobs = [
            JobRequestBody(project_id=123, timezone="UTC", created_by="test"),
            JobRequestBody(project_id=456, timezone="UTC", created_by="test"),
        ]
        result = client._serialize_body(jobs)
        assert len(result) == 2
        assert result[0]["projectId"] == 123
        assert result[1]["projectId"] == 456

    def test_to_camel_case(self, client):
        """Test snake_case to camelCase conversion."""
        assert client._to_camel_case("project_id") == "projectId"
        assert client._to_camel_case("created_by") == "createdBy"
        assert client._to_camel_case("api_key") == "apiKey"
        assert client._to_camel_case("simple") == "simple"


class TestClientHTTPMethods:
    """Test HTTP method wrappers."""

    @patch('scheduler0.client.Client._request')
    def test_get(self, mock_request, client):
        """Test GET request."""
        mock_request.return_value.json.return_value = {"success": True}
        result = client._get("/jobs")
        assert result == {"success": True}
        mock_request.assert_called_once_with(
            "GET", "/jobs", body=None, params=None, account_id_override=None
        )

    @patch('scheduler0.client.Client._request')
    def test_post(self, mock_request, client):
        """Test POST request."""
        mock_request.return_value.status_code = 201
        mock_request.return_value.json.return_value = {"success": True}
        body = {"test": "data"}
        result = client._post("/jobs", body)
        assert result == {"success": True}
        mock_request.assert_called_once_with(
            "POST", "/jobs", body=body, params=None, account_id_override=None
        )

    @patch('scheduler0.client.Client._request')
    def test_post_204_no_content(self, mock_request, client):
        """Test POST request with 204 No Content."""
        mock_request.return_value.status_code = 204
        result = client._post("/jobs")
        assert result == {}

    @patch('scheduler0.client.Client._request')
    def test_put(self, mock_request, client):
        """Test PUT request."""
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {"success": True}
        body = {"test": "data"}
        result = client._put("/jobs/1", body)
        assert result == {"success": True}

    @patch('scheduler0.client.Client._request')
    def test_delete(self, mock_request, client):
        """Test DELETE request."""
        mock_request.return_value.status_code = 204
        client._delete("/jobs/1")
        mock_request.assert_called_once_with(
            "DELETE", "/jobs/1", body=None, params=None, account_id_override=None
        )


class TestClientErrorHandling:
    """Test error handling."""

    def test_request_http_error(self, client):
        """Test HTTP error handling."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_response.json.return_value = {"message": "Invalid request"}
        client.session.request = Mock(return_value=mock_response)

        with pytest.raises(requests.HTTPError) as exc_info:
            client._request("GET", "/jobs")
        assert "Invalid request" in str(exc_info.value)

    def test_request_http_error_no_json(self, client):
        """Test HTTP error handling when response is not JSON."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.json.side_effect = ValueError("Not JSON")
        client.session.request = Mock(return_value=mock_response)

        with pytest.raises(requests.HTTPError) as exc_info:
            client._request("GET", "/jobs")
        assert "Internal Server Error" in str(exc_info.value)

    def test_request_network_error(self, client):
        """Test network error handling."""
        client.session.request = Mock(side_effect=requests.ConnectionError("Connection failed"))

        with pytest.raises(requests.ConnectionError):
            client._request("GET", "/jobs")

