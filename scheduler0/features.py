"""
Feature management methods for Scheduler0 client.
"""

from .client import Client


def list_features(self: Client) -> dict:
    """List all available features."""
    return self._get("/features")


# Attach methods to Client class
Client.list_features = list_features

