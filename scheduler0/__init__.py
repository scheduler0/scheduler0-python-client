"""
Scheduler0 Python Client

A Python client library for interacting with the Scheduler0 API.
"""

from .client import Client, NewClient, NewAPIClient, NewAPIClientWithAccount, NewBasicAuthClient

# Import all modules to attach methods to Client class
from . import accounts
from . import credentials
from . import jobs
from . import projects
from . import executors
from . import executions
from . import features
from . import async_tasks
from . import healthcheck
from . import prompt

# Import types
from .types import (
    Account,
    AccountCreateRequestBody,
    AccountFeature,
    Credential,
    CredentialCreateRequestBody,
    CredentialUpdateRequestBody,
    CredentialDeleteRequestBody,
    CredentialArchiveRequestBody,
    Job,
    JobRequestBody,
    JobUpdateRequestBody,
    JobDeleteRequestBody,
    Project,
    ProjectRequestBody,
    ProjectUpdateRequestBody,
    ProjectDeleteRequestBody,
    Executor,
    ExecutorRequestBody,
    ExecutorUpdateRequestBody,
    ExecutorDeleteRequestBody,
    Execution,
    Feature,
    FeatureRequest,
    AsyncTask,
    HealthcheckData,
    RaftStats,
    PromptJobRequest,
    PromptJobResponse,
)

__version__ = "1.0.0"
__all__ = [
    "Client",
    "NewClient",
    "NewAPIClient",
    "NewAPIClientWithAccount",
    "NewBasicAuthClient",
    # Types
    "Account",
    "AccountCreateRequestBody",
    "AccountFeature",
    "Credential",
    "CredentialCreateRequestBody",
    "CredentialUpdateRequestBody",
    "CredentialDeleteRequestBody",
    "CredentialArchiveRequestBody",
    "Job",
    "JobRequestBody",
    "JobUpdateRequestBody",
    "JobDeleteRequestBody",
    "Project",
    "ProjectRequestBody",
    "ProjectUpdateRequestBody",
    "ProjectDeleteRequestBody",
    "Executor",
    "ExecutorRequestBody",
    "ExecutorUpdateRequestBody",
    "ExecutorDeleteRequestBody",
    "Execution",
    "Feature",
    "FeatureRequest",
    "AsyncTask",
    "HealthcheckData",
    "RaftStats",
    "PromptJobRequest",
    "PromptJobResponse",
]

