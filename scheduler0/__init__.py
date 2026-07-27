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
from . import suggestions
from . import schedule
from . import backup
from . import local_executors

# Import types
from .types import (
    Account,
    AccountCreateRequestBody,
    AccountUpdateRequestBody,
    AccountFeature,
    AccountJobExecutionsCount,
    AccountClassifyRequestsCount,
    AccountPromptRequestsCount,
    AccountAISettings,
    ActiveModel,
    ModelInfo,
    PromptRequest,
    PromptRequestsResult,
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
    TestInvocationRequestBody,
    JobInvocationPayload,
    TestInvocationResult,
    Execution,
    Feature,
    FeatureRequest,
    AsyncTask,
    HealthcheckData,
    RaftStats,
    PromptJobRequest,
    PromptJobResponse,
    SuggestionParticipant,
    SuggestionMessage,
    SuggestionOptions,
    AnalyzeSuggestionsRequest,
    AnalyzeSuggestionsResult,
    SendTimeWorkingHours,
    SendTimeQuietHours,
    SendTimeParticipant,
    SendTimeMessage,
    SendTimeConstraints,
    SendTimeWindow,
    SendTimePreferences,
    SendTimeGroupPolicy,
    SendTimeOptions,
    SendTimeHolidayPolicy,
    SendTimeBusyInterval,
    SendTimeAvailability,
    SendTimeSuggestionsRequest,
    SendTimeSuggestionsResult,
    ScheduleProjectInput,
    SchedulePromptRequest,
    ScheduleResult,
    LocalExecutorRegisterRequest,
    LocalExecutionReport,
)

__version__ = "1.2.0"
__all__ = [
    "Client",
    "NewClient",
    "NewAPIClient",
    "NewAPIClientWithAccount",
    "NewBasicAuthClient",
    # Types
    "Account",
    "AccountCreateRequestBody",
    "AccountUpdateRequestBody",
    "AccountFeature",
    "AccountJobExecutionsCount",
    "AccountClassifyRequestsCount",
    "AccountPromptRequestsCount",
    "AccountAISettings",
    "PromptRequest",
    "PromptRequestsResult",
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
    "TestInvocationRequestBody",
    "JobInvocationPayload",
    "TestInvocationResult",
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
    "SuggestionParticipant",
    "SuggestionMessage",
    "SuggestionOptions",
    "AnalyzeSuggestionsRequest",
    "AnalyzeSuggestionsResult",
    "SendTimeWorkingHours",
    "SendTimeQuietHours",
    "SendTimeParticipant",
    "SendTimeMessage",
    "SendTimeConstraints",
    "SendTimeWindow",
    "SendTimePreferences",
    "SendTimeGroupPolicy",
    "SendTimeOptions",
    "SendTimeHolidayPolicy",
    "SendTimeBusyInterval",
    "SendTimeAvailability",
    "SendTimeSuggestionsRequest",
    "SendTimeSuggestionsResult",
    "ScheduleProjectInput",
    "SchedulePromptRequest",
    "ScheduleResult",
    "LocalExecutorRegisterRequest",
    "LocalExecutionReport",
]

