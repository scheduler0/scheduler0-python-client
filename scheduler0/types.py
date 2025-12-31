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


# Credential Types
@dataclass
class Credential:
    id: int
    account_id: int
    archived: bool
    api_key: str
    api_secret: str
    date_created: str
    date_modified: Optional[str] = None
    date_deleted: Optional[str] = None
    created_by: Optional[str] = None
    modified_by: Optional[str] = None
    deleted_by: Optional[str] = None
    archived_by: Optional[str] = None


@dataclass
class CredentialCreateRequestBody:
    created_by: str
    archived: bool = False
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
    id: int
    account_id: int
    name: str
    type: str
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

