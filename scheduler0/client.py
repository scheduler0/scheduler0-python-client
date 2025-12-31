"""
Core client implementation for Scheduler0 Python client.
"""

from typing import Optional, Dict, Any, List
from urllib.parse import urljoin, urlparse

import requests


class Client:
    """
    Scheduler0 API client.

    Supports multiple authentication methods:
    - API Key + Secret authentication (default)
    - Basic authentication (for peer communication)
    """

    def __init__(
        self,
        base_url: str,
        version: str = "v1",
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        account_id: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """
        Initialize a new Scheduler0 client.

        Args:
            base_url: Base URL of the Scheduler0 API (e.g., "http://localhost:7070")
            version: API version (default: "v1")
            api_key: API key for authentication
            api_secret: API secret for authentication
            account_id: Account ID for requests
            username: Username for basic authentication
            password: Password for basic authentication
        """
        parsed_url = urlparse(base_url)
        if not parsed_url.scheme or parsed_url.scheme not in ('http', 'https'):
            raise ValueError("base_url must include a scheme (http:// or https://)")

        self.base_url = base_url.rstrip("/")
        self.version = version
        self.api_key = api_key
        self.api_secret = api_secret
        self.account_id = account_id
        self.username = username
        self.password = password
        self.session = requests.Session()

    def _resolve_account_id(
        self, body: Optional[Any] = None, account_id_override: Optional[str] = None
    ) -> Optional[str]:
        """Resolve account ID from override, body, or client default."""
        if account_id_override:
            return account_id_override

        if body and hasattr(body, "account_id") and body.account_id:
            return str(body.account_id)

        return self.account_id

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        endpoint = endpoint.lstrip("/")
        version_prefix = f"/api/{self.version}/"
        return urljoin(self.base_url + version_prefix, endpoint)

    def _prepare_headers(
        self,
        account_id: Optional[str] = None,
    ) -> Dict[str, str]:
        """Prepare request headers with authentication."""
        headers = {"Content-Type": "application/json"}

        # Set authentication
        if self.username and self.password:
            # Basic Auth for peer communication
            headers["X-Peer"] = "cmd"
        elif self.api_key and self.api_secret:
            # API Key + Secret authentication
            headers["X-API-Key"] = self.api_key
            headers["X-API-Secret"] = self.api_secret

        # Add account ID if provided
        if account_id:
            headers["X-Account-ID"] = account_id

        return headers

    def _request(
        self,
        method: str,
        endpoint: str,
        body: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        account_id_override: Optional[str] = None,
    ) -> requests.Response:
        """
        Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., "/jobs", "/projects/123")
            body: Request body (will be JSON encoded)
            params: Query parameters
            account_id_override: Optional account ID override

        Returns:
            Response object

        Raises:
            requests.HTTPError: If the request fails
        """
        url = self._build_url(endpoint)
        account_id = self._resolve_account_id(body, account_id_override)
        headers = self._prepare_headers(account_id)

        # Prepare request data
        json_data = None
        if body is not None:
            json_data = self._serialize_body(body)

        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            json=json_data,
            params=params,
            auth=(self.username, self.password) if self.username and self.password else None,
        )

        # Raise exception for error status codes
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

        return response

    def _to_camel_case(self, snake_str: str) -> str:
        """Convert snake_case to camelCase."""
        components = snake_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    def _serialize_body(self, body: Any) -> Any:
        """Serialize request body to JSON-serializable format."""
        if body is None:
            return None

        # Handle dataclasses
        if hasattr(body, "__dataclass_fields__"):
            result = {}
            for key, value in body.__dict__.items():
                if key != "account_id" and value is not None:
                    camel_key = self._to_camel_case(key)
                    result[camel_key] = self._serialize_value(value)
            return result

        # Handle regular objects with __dict__
        if hasattr(body, "__dict__"):
            result = {}
            for key, value in body.__dict__.items():
                if key != "account_id" and value is not None:
                    camel_key = self._to_camel_case(key)
                    result[camel_key] = self._serialize_value(value)
            return result

        # Handle dictionaries
        if isinstance(body, dict):
            result = {}
            for key, value in body.items():
                if key != "account_id" and value is not None:
                    camel_key = self._to_camel_case(key) if isinstance(key, str) else key
                    result[camel_key] = self._serialize_value(value)
            return result

        # Handle lists
        if isinstance(body, list):
            return [self._serialize_body(item) for item in body]

        # Handle primitive types
        return body

    def _serialize_value(self, value: Any) -> Any:
        """Recursively serialize a value."""
        if value is None:
            return None

        # Handle dataclasses
        if hasattr(value, "__dataclass_fields__"):
            return self._serialize_body(value)

        # Handle lists
        if isinstance(value, list):
            return [self._serialize_value(item) for item in value]

        # Handle dictionaries
        if isinstance(value, dict):
            return {k: self._serialize_value(v) for k, v in value.items()}

        # Handle primitive types
        return value

    def _get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        account_id_override: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Make a GET request."""
        response = self._request("GET", endpoint, body=None, params=params, account_id_override=account_id_override)
        return response.json()

    def _post(
        self,
        endpoint: str,
        body: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        account_id_override: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Make a POST request."""
        response = self._request("POST", endpoint, body=body, params=params, account_id_override=account_id_override)
        if response.status_code == 204:
            return {}
        return response.json()

    def _put(
        self,
        endpoint: str,
        body: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        account_id_override: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Make a PUT request."""
        response = self._request("PUT", endpoint, body=body, params=params, account_id_override=account_id_override)
        if response.status_code == 204:
            return {}
        return response.json()

    def _delete(
        self,
        endpoint: str,
        body: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        account_id_override: Optional[str] = None,
    ) -> None:
        """Make a DELETE request."""
        self._request("DELETE", endpoint, body=body, params=params, account_id_override=account_id_override)


# Convenience factory functions

def NewClient(
    base_url: str,
    version: str = "v1",
    api_key: Optional[str] = None,
    api_secret: Optional[str] = None,
    account_id: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> Client:
    """
    Create a new Scheduler0 client with flexible options.

    Args:
        base_url: Base URL of the Scheduler0 API
        version: API version (default: "v1")
        api_key: API key for authentication
        api_secret: API secret for authentication
        account_id: Account ID for requests
        username: Username for basic authentication
        password: Password for basic authentication

    Returns:
        Client instance
    """
    return Client(
        base_url=base_url,
        version=version,
        api_key=api_key,
        api_secret=api_secret,
        account_id=account_id,
        username=username,
        password=password,
    )


def NewAPIClient(
    base_url: str,
    version: str,
    api_key: str,
    api_secret: str,
) -> Client:
    """
    Create a client with API key authentication.

    Args:
        base_url: Base URL of the Scheduler0 API
        version: API version
        api_key: API key
        api_secret: API secret

    Returns:
        Client instance
    """
    return Client(
        base_url=base_url,
        version=version,
        api_key=api_key,
        api_secret=api_secret,
    )


def NewAPIClientWithAccount(
    base_url: str,
    version: str,
    api_key: str,
    api_secret: str,
    account_id: str,
) -> Client:
    """
    Create a client with API key authentication and account ID.

    Args:
        base_url: Base URL of the Scheduler0 API
        version: API version
        api_key: API key
        api_secret: API secret
        account_id: Account ID

    Returns:
        Client instance
    """
    return Client(
        base_url=base_url,
        version=version,
        api_key=api_key,
        api_secret=api_secret,
        account_id=account_id,
    )


def NewBasicAuthClient(
    base_url: str,
    version: str,
    username: str,
    password: str,
) -> Client:
    """
    Create a client with basic authentication for peer communication.

    Args:
        base_url: Base URL of the Scheduler0 API
        version: API version
        username: Username
        password: Password

    Returns:
        Client instance
    """
    return Client(
        base_url=base_url,
        version=version,
        username=username,
        password=password,
    )

