"""
AI-powered job creation methods for Scheduler0 client.
"""

from typing import Optional, List, Dict, Any
from .client import Client
from .types import PromptJobRequest


def create_job_from_prompt(
    self: Client,
    body: PromptJobRequest,
    account_id_override: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Create job configurations from natural language prompts using AI.

    Note: This endpoint requires credits and validates credentials.
    1 credit per prompt execution.

    Args:
        body: Prompt job request with prompt and optional metadata
        account_id_override: Optional account ID override

    Returns:
        List of PromptJobResponse dictionaries with generated configurations
    """
    response = self._request("POST", "/prompt", body=body, account_id_override=account_id_override)
    return response.json()  # Returns a list directly, not wrapped in a dict


# Attach methods to Client class
Client.create_job_from_prompt = create_job_from_prompt

