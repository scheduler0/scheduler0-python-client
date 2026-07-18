"""
Type definitions for Scheduler0 Python client.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


# Account Types
@dataclass
class AccountFeature:
    account_id: int
    feature_id: int
    feature: str


@dataclass
class Account:
    id: int
    name: str
    features: List[AccountFeature] = field(default_factory=list)
    date_created: Optional[str] = None
    date_modified: Optional[str] = None


@dataclass
class AccountCreateRequestBody:
    name: str
    account_id: Optional[int] = None  # Excluded from JSON


@dataclass
class AccountUpdateRequestBody:
    name: str
    account_id: Optional[int] = None  # Excluded from JSON


@dataclass
class AccountJobExecutionsCount:
    id: int
    account_id: int
    execution_count: int
    tokens: int
    date_created: str
    date_modified: str
    next_reset_date: str


@dataclass
class AccountClassifyRequestsCount:
    """Remaining monthly AI classify-request quota for an account."""
    id: int
    account_id: int
    request_count: int
    date_created: str
    date_modified: str
    next_reset_date: str


@dataclass
class AccountPromptRequestsCount:
    """Remaining monthly AI prompt-request quota for an account."""
    id: int
    account_id: int
    request_count: int
    date_created: str
    date_modified: str
    next_reset_date: str


@dataclass
class ActiveModel:
    """A single entry in the ordered active-model list."""
    provider: str
    model: str


@dataclass
class ModelInfo:
    """Approved model info returned by get_ai_models()."""
    id: str
    display_name: str
    default: Optional[bool] = None


@dataclass
class AccountAISettings:
    account_id: Optional[int] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    active_models: Optional[List[ActiveModel]] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    bedrock_access_key_id: Optional[str] = None
    bedrock_secret_key: Optional[str] = None
    bedrock_region: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    date_created: Optional[str] = None
    date_modified: Optional[str] = None


# Credential Types
@dataclass
class Credential:
    """Credential returned by the Scheduler0 API.

    ``api_secret`` (the AES-GCM encrypted form) is **never** included in API
    responses.  ``plaintext_secret`` is returned exactly once in the 201 create
    response — the server cannot retrieve it afterwards.  Save it immediately.
    """
    id: int
    account_id: int
    archived: bool
    api_key: str
    date_created: str
    date_modified: Optional[str] = None
    date_deleted: Optional[str] = None
    created_by: Optional[str] = None
    modified_by: Optional[str] = None
    deleted_by: Optional[str] = None
    archived_by: Optional[str] = None
    expires_at: Optional[str] = None
    scopes: List[str] = field(default_factory=list)
    plaintext_secret: Optional[str] = None


@dataclass
class RotateSecretData:
    """Payload returned by rotate_secret()."""
    credentials_rotated: int
    executors_rotated: int
    ai_settings_rotated: int


@dataclass
class RotateSecretResponse:
    """Response returned by rotate_secret()."""
    success: bool
    data: RotateSecretData


@dataclass
class CredentialCreateRequestBody:
    created_by: str
    # Scopes must be a non-empty subset of {"read", "write", "execute", "admin"};
    # the API rejects empty/unknown values with a 400. The "admin" scope can only
    # be granted by an operator or an existing admin credential.
    scopes: List[str] = field(default_factory=list)
    archived: bool = False
    # Optional shorter lifetime in seconds. The server clamps it to its allowed
    # range; leave as None to use the default expiry. Serialized as expiresInSeconds.
    expires_in_seconds: Optional[int] = None
    account_id: Optional[int] = None  # Excluded from JSON


@dataclass
class CredentialUpdateRequestBody:
    modified_by: str
    archived: bool = False
    account_id: Optional[int] = None  # Excluded from JSON


@dataclass
class CredentialDeleteRequestBody:
    deleted_by: str
    account_id: Optional[int] = None  # Excluded from JSON


@dataclass
class CredentialArchiveRequestBody:
    archived_by: str
    account_id: Optional[int] = None  # Excluded from JSON


# Job Types
@dataclass
class Job:
    id: Optional[int] = None
    account_id: Optional[int] = None
    project_id: Optional[int] = None
    executor_id: Optional[int] = None
    data: Optional[str] = None
    spec: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    last_execution_date: Optional[str] = None
    timezone: Optional[str] = None
    timezone_offset: Optional[int] = None
    retry_max: Optional[int] = None
    execution_id: Optional[str] = None
    status: Optional[str] = None
    date_created: Optional[str] = None
    date_modified: Optional[str] = None
    created_by: Optional[str] = None
    modified_by: Optional[str] = None
    deleted_by: Optional[str] = None


@dataclass
class JobRequestBody:
    project_id: int
    timezone: str
    executor_id: Optional[int] = None
    data: Optional[str] = None
    spec: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    timezone_offset: Optional[int] = None
    retry_max: Optional[int] = None
    status: Optional[str] = None
    created_by: Optional[str] = None
    account_id: Optional[int] = None  # Excluded from JSON


@dataclass
class JobUpdateRequestBody:
    modified_by: str
    project_id: Optional[int] = None
    executor_id: Optional[int] = None
    data: Optional[str] = None
    spec: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    timezone: Optional[str] = None
    timezone_offset: Optional[int] = None
    retry_max: Optional[int] = None
    status: Optional[str] = None
    account_id: Optional[int] = None  # Excluded from JSON


@dataclass
class JobDeleteRequestBody:
    deleted_by: str
    account_id: Optional[int] = None  # Excluded from JSON


# Project Types
@dataclass
class Project:
    id: int
    account_id: int
    name: str
    description: str
    date_created: str
    date_modified: Optional[str] = None
    created_by: Optional[str] = None
    modified_by: Optional[str] = None
    deleted_by: Optional[str] = None


@dataclass
class ProjectRequestBody:
    name: str
    description: str
    created_by: str
    account_id: Optional[int] = None  # Excluded from JSON


@dataclass
class ProjectUpdateRequestBody:
    description: str
    modified_by: str
    account_id: Optional[int] = None  # Excluded from JSON


@dataclass
class ProjectDeleteRequestBody:
    deleted_by: str
    account_id: Optional[int] = None  # Excluded from JSON


# Executor Types
@dataclass
class Executor:
    # cloud_api_key, cloud_api_secret and webhook_secret are secrets. The server stores
    # them encrypted and only returns them once, in the create_executor response. They are
    # always None on get_executor, list_executors and update_executor responses.
    id: int
    account_id: int
    name: str
    type: str
    # description and tags describe what the executor does. They are used by the
    # /ai/schedule endpoint to match an executor to a prompt's purpose and channels.
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    region: Optional[str] = None
    cloud_provider: Optional[str] = None
    cloud_resource_url: Optional[str] = None
    cloud_api_key: Optional[str] = None
    cloud_api_secret: Optional[str] = None
    webhook_url: Optional[str] = None
    webhook_secret: Optional[str] = None
    webhook_method: Optional[str] = None
    date_created: Optional[str] = None
    date_modified: Optional[str] = None
    date_deleted: Optional[str] = None
    created_by: Optional[str] = None
    modified_by: Optional[str] = None
    deleted_by: Optional[str] = None


@dataclass
class ExecutorRequestBody:
    name: str
    type: str
    created_by: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    region: Optional[str] = None
    cloud_provider: Optional[str] = None
    cloud_resource_url: Optional[str] = None
    cloud_api_key: Optional[str] = None
    cloud_api_secret: Optional[str] = None
    webhook_url: Optional[str] = None
    webhook_secret: Optional[str] = None
    webhook_method: Optional[str] = None
    account_id: Optional[int] = None  # Excluded from JSON


@dataclass
class ExecutorUpdateRequestBody:
    name: str
    type: str
    modified_by: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    region: Optional[str] = None
    cloud_provider: Optional[str] = None
    cloud_resource_url: Optional[str] = None
    cloud_api_key: Optional[str] = None
    cloud_api_secret: Optional[str] = None
    webhook_url: Optional[str] = None
    webhook_secret: Optional[str] = None
    webhook_method: Optional[str] = None
    account_id: Optional[int] = None  # Excluded from JSON


@dataclass
class ExecutorDeleteRequestBody:
    deleted_by: str
    account_id: Optional[int] = None  # Excluded from JSON


# Execution Types
@dataclass
class Execution:
    id: int
    account_id: int
    unique_id: str
    state: int
    node_id: int
    job_id: int
    last_execution_datetime: Optional[str] = None
    next_execution_datetime: Optional[str] = None
    job_queue_version: Optional[int] = None
    execution_version: Optional[int] = None
    date_created: Optional[str] = None
    date_modified: Optional[str] = None


# Feature Types
@dataclass
class Feature:
    id: int
    name: str
    date_created: Optional[str] = None
    date_modified: Optional[str] = None


@dataclass
class FeatureRequest:
    feature_id: int
    account_id: Optional[int] = None  # Excluded from JSON


# Async Task Types
@dataclass
class AsyncTask:
    id: int
    request_id: str
    input: str
    output: str
    service: str
    state: int
    date_created: str


# Healthcheck Types
@dataclass
class RaftStats:
    applied_index: str
    commit_index: str
    fsm_pending: str
    last_contact: str
    last_log_index: str
    last_log_term: str
    last_snapshot_index: str
    last_snapshot_term: str
    latest_configuration: str
    latest_configuration_index: str
    num_peers: str
    protocol_version: str
    protocol_version_max: str
    protocol_version_min: str
    snapshot_version_max: str
    snapshot_version_min: str
    state: str
    term: str


@dataclass
class HealthcheckData:
    leader_address: str
    leader_id: str
    raft_stats: RaftStats


# Prompt Types
@dataclass
class PromptJobRequest:
    prompt: str
    purposes: Optional[List[str]] = None
    events: Optional[List[str]] = None
    recipients: Optional[List[str]] = None
    channels: Optional[List[str]] = None
    timezone: Optional[str] = None
    # Optional BCP-47 locale (e.g. "en-US", "es-ES") forwarded to the AI model;
    # omitted falls back to "en".
    locale: Optional[str] = None


@dataclass
class PromptJobResponse:
    kind: Optional[str] = None
    purpose: Optional[str] = None
    subject: Optional[str] = None
    next_run_at: Optional[str] = None
    recurrence: Optional[str] = None
    event: Optional[str] = None
    delivery: Optional[str] = None
    cron_expression: Optional[str] = None
    channel: Optional[str] = None
    recipients: Optional[List[str]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    timezone: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class PromptProviderResult:
    provider: str
    model: str
    jobs: List[PromptJobResponse]
    input_tokens: int
    output_tokens: int
    total_tokens: int
    duration_ms: int


@dataclass
class IntentClassification:
    text: str = ""
    decision: str = ""
    reason: str = ""


@dataclass
class PromptResult:
    providers: List[PromptProviderResult] = field(default_factory=list)
    classification: Optional[IntentClassification] = None


@dataclass
class PromptRequest:
    """A single persisted AI prompt execution from the prompt-request log."""
    id: int = 0
    account_id: int = 0
    prompt: str = ""
    provider: str = ""
    model: str = ""
    output: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    duration_ms: int = 0
    estimated_cost_usd: float = 0.0
    status: str = ""
    error: Optional[str] = None
    date_created: str = ""


@dataclass
class PromptRequestsResult:
    """Paginated result for the AI prompt-request log."""
    requests: List[PromptRequest] = field(default_factory=list)
    total: int = 0
    limit: int = 0
    offset: int = 0


@dataclass
class ClassifyPromptRequest:
    prompt: str
    # Optional BCP-47 locale. Only English (en*) is currently supported; other
    # locales are rejected by the server with a 400.
    locale: Optional[str] = None


# Schedule-from-prompt Types (POST /ai/schedule)
@dataclass
class ScheduleProjectInput:
    """Create-or-reuse a project by name. Ignored when project_id is set."""
    name: Optional[str] = None
    description: Optional[str] = None


@dataclass
class SchedulePromptRequest:
    prompt: str
    purposes: Optional[List[str]] = None
    events: Optional[List[str]] = None
    recipients: Optional[List[str]] = None
    channels: Optional[List[str]] = None
    timezone: Optional[str] = None
    locale: Optional[str] = None
    # project_id reuses an existing project; takes precedence over project.
    project_id: Optional[int] = None
    # project creates-or-reuses a project by name when project_id is absent.
    project: Optional[ScheduleProjectInput] = None
    # executor_id pins a specific executor and skips LLM matching.
    executor_id: Optional[int] = None
    # created_by is required; stamped on the created project and jobs.
    created_by: Optional[str] = None
    account_id: Optional[int] = None  # Excluded from JSON


@dataclass
class ScheduleResult:
    classification: Optional[IntentClassification] = None
    project: Optional[Dict[str, Any]] = None
    project_created: bool = False
    executor: Optional[Dict[str, Any]] = None
    executor_matched_by: str = ""
    executor_match_reason: Optional[str] = None
    jobs: List[Dict[str, Any]] = field(default_factory=list)
    provider: Optional[str] = None
    model: Optional[str] = None


# Conversation Suggestions Types
@dataclass
class SuggestionParticipant:
    id: Optional[str] = None
    display_name: Optional[str] = None
    timezone: Optional[str] = None


@dataclass
class SuggestionMessage:
    # speaker accepts a SuggestionParticipant or a bare display-name string.
    speaker: Any
    timestamp: str
    message: str
    id: Optional[str] = None


@dataclass
class SuggestionOptions:
    """Analysis options.

    locale is English only for the first release: it defaults to ``en`` and only
    accepts ``en*`` values; any other locale is rejected by the API with
    UNSUPPORTED_LOCALE.
    """

    reference_time: Optional[str] = None
    locale: Optional[str] = None
    default_timezone: Optional[str] = None
    minimum_confidence: Optional[float] = None
    include_low_confidence: Optional[bool] = None
    include_resolved_obligations: Optional[bool] = None
    default_due_time: Optional[str] = None
    default_deadline_time: Optional[str] = None


@dataclass
class AnalyzeSuggestionsRequest:
    messages: List[SuggestionMessage] = field(default_factory=list)
    conversation_id: Optional[str] = None
    participants: Optional[List[SuggestionParticipant]] = None
    options: Optional[SuggestionOptions] = None


@dataclass
class AnalyzeSuggestionsResult:
    """The analyzer's response.

    Individual suggestions/obligations carry a rich, evolving shape owned by the
    edge analyzer, so they are exposed as plain dicts.
    """

    request_id: Optional[str] = None
    conversation_id: Optional[str] = None
    analyzed_at: Optional[str] = None
    suggestions: List[Dict[str, Any]] = field(default_factory=list)
    obligations: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[Dict[str, Any]] = field(default_factory=list)
    engine: Optional[Dict[str, Any]] = None


# Send-Time Suggestions Types
# The engine is deterministic scheduling/time-zone math (no LLM). All field names
# are snake_case to match the API contract.
@dataclass
class SendTimeWorkingHours:
    days: Optional[List[str]] = None
    start: Optional[str] = None
    end: Optional[str] = None


@dataclass
class SendTimeQuietHours:
    start: Optional[str] = None
    end: Optional[str] = None


@dataclass
class SendTimeParticipant:
    timezone: str
    id: Optional[str] = None
    display_name: Optional[str] = None
    role: Optional[str] = None
    working_hours: Optional[SendTimeWorkingHours] = None
    quiet_hours: Optional[SendTimeQuietHours] = None


@dataclass
class SendTimeMessage:
    channel: Optional[str] = None
    priority: Optional[str] = None
    intent: Optional[str] = None
    text: Optional[str] = None
    estimated_attention: Optional[str] = None


@dataclass
class SendTimeConstraints:
    earliest_send_at: Optional[str] = None
    latest_send_at: Optional[str] = None
    minimum_delay_seconds: Optional[int] = None
    working_hours_only: Optional[bool] = None
    avoid_weekends: Optional[bool] = None
    avoid_holidays: Optional[bool] = None
    respect_quiet_hours: Optional[bool] = None
    require_calendar_free: Optional[bool] = None


@dataclass
class SendTimeWindow:
    start: str
    end: str


@dataclass
class SendTimePreferences:
    preferred_recipient_windows: Optional[List[SendTimeWindow]] = None
    avoid_recipient_windows: Optional[List[SendTimeWindow]] = None
    prefer_sender_recipient_overlap: Optional[bool] = None


@dataclass
class SendTimeGroupPolicy:
    strategy: Optional[str] = None
    minimum_recipient_coverage: Optional[float] = None


@dataclass
class SendTimeOptions:
    reference_time: Optional[str] = None
    suggestion_count: Optional[int] = None
    candidate_interval_minutes: Optional[int] = None
    locale: Optional[str] = None
    include_score_breakdown: Optional[bool] = None
    include_rejected_summary: Optional[bool] = None
    search_horizon_days: Optional[int] = None
    evaluate_send_now: Optional[bool] = None
    diversify_suggestions: Optional[bool] = None
    minimum_suggestion_spacing_minutes: Optional[int] = None


@dataclass
class SendTimeHolidayPolicy:
    country: Optional[str] = None
    region: Optional[str] = None
    calendar_id: Optional[str] = None
    dates: Optional[List[str]] = None


@dataclass
class SendTimeBusyInterval:
    start: str
    end: str


@dataclass
class SendTimeAvailability:
    participant_id: str
    busy_intervals: Optional[List[SendTimeBusyInterval]] = None


@dataclass
class SendTimeSuggestionsRequest:
    recipients: List[SendTimeParticipant] = field(default_factory=list)
    sender: Optional[SendTimeParticipant] = None
    message: Optional[SendTimeMessage] = None
    constraints: Optional[SendTimeConstraints] = None
    preferences: Optional[SendTimePreferences] = None
    group_policy: Optional[SendTimeGroupPolicy] = None
    options: Optional[SendTimeOptions] = None
    holiday_policy: Optional[SendTimeHolidayPolicy] = None
    availability: Optional[List[SendTimeAvailability]] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class SendTimeSuggestionsResult:
    """The send-time engine's response.

    The top-level fields are typed; individual suggestions and the search /
    send_now blocks carry a rich, evolving shape, so they are exposed as dicts.
    """

    request_id: Optional[str] = None
    reference_time: Optional[str] = None
    policy: Optional[Dict[str, Any]] = None
    engine: Optional[Dict[str, Any]] = None
    suggestions: List[Dict[str, Any]] = field(default_factory=list)
    search: Optional[Dict[str, Any]] = None
    rejected_summary: Optional[Dict[str, int]] = None
    no_suggestion: Optional[Dict[str, Any]] = None
    send_now: Optional[Dict[str, Any]] = None
    warnings: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None


# Execution Analytics Types
@dataclass
class DateRangeAnalyticsPoint:
    date: str
    time: str
    scheduled: int
    success: int
    failed: int


@dataclass
class DateRangeAnalyticsResponse:
    account_id: int
    timezone: str
    start_date: str
    start_time: str
    end_date: str
    end_time: str
    points: List[DateRangeAnalyticsPoint]


@dataclass
class ExecutionTotalsResponse:
    account_id: int
    scheduled: int
    success: int
    failed: int


@dataclass
class CleanupOldLogsRequestBody:
    account_id: str
    retention_months: int


@dataclass
class CleanupOldLogsResponse:
    success: bool
    data: Dict[str, Any]


# Local Executor Types
@dataclass
class LocalExecutorRegisterRequest:
    """Body for POST /local-executors. The server sets the executor type to "local"."""
    name: str
    command: str
    working_dir: Optional[str] = None
    created_by: Optional[str] = None


@dataclass
class LocalExecutionReport:
    """A single execution event reported to POST /local-executors/{id}/executions.

    ``state`` is an integer: 0 = scheduled, 1 = success, 2 = failed.
    ``last_execution_time`` / ``next_execution_time`` are RFC3339 strings.
    """
    job_id: int
    unique_id: str
    state: int
    last_execution_time: Optional[str] = None
    next_execution_time: Optional[str] = None
    execution_version: Optional[int] = None
    job_queue_version: Optional[int] = None

