"""
Healthcheck methods for Scheduler0 client.
"""

from .client import Client


def healthcheck(self: Client) -> dict:
    """Check cluster health (no authentication required)."""
    return self._get("/healthcheck")


# Attach methods to Client class
Client.healthcheck = healthcheck

