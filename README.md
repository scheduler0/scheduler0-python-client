<div align="center">
  <img src="https://raw.githubusercontent.com/scheduler0/scheduler0-python-client/main/logo.png" alt="Scheduler0 Logo" width="200"/>
</div>

# Scheduler0 Python Client

Python client for the [Scheduler0](https://scheduler0.com) HTTP API (`/api/v1`). It is a thin, synchronous wrapper over [`requests`](https://requests.readthedocs.io/): every method builds the request, sets the auth headers, and returns the decoded JSON envelope (`{"success": bool, "data": ...}`) as a `dict`, except the AI methods noted below which return typed dataclasses.

- Full API reference: [api-reference.scheduler0.com](https://api-reference.scheduler0.com)
- Docs: [docs.scheduler0.com](https://docs.scheduler0.com)

## Installation

```bash
pip install scheduler0
```

Requires Python 3.8+ and `requests>=2.28`.

## Authentication and configuration

Every request except `healthcheck()` needs three headers, which the client sets from its constructor arguments:

| Header | Source |
|--------|--------|
| `X-API-Key` | `api_key` |
| `X-Secret-Key` | `api_secret` |
| `X-Account-ID` | `account_id` (or a per-call `account_id_override`) |

```python
from scheduler0 import Client

client = Client(
    base_url="https://api.scheduler0.com",  # required; must include http:// or https://
    version="v1",                           # optional, default "v1"
    api_key="your-api-key",
    api_secret="your-api-secret",
    account_id="123",
)
```

`NewClient(...)`, `NewAPIClient(base_url, version, api_key, api_secret)`, `NewAPIClientWithAccount(base_url, version, api_key, api_secret, account_id)` and `NewBasicAuthClient(base_url, version, username, password)` are equivalent factory functions.

Notes on behaviour, as implemented in `scheduler0/client.py`:

- There is no default `base_url`; the hosted API is `https://api.scheduler0.com`. For a self-hosted cluster use your own URL.
- Requests are made with a `requests.Session` and **no timeout**. Set one yourself if you need it (e.g. wrap calls or mount an adapter on `client.session`).
- There are no automatic retries, rate-limit handling or pagination helpers.
- The account ID resolves in this order: `account_id_override` argument, the body's `account_id` field (never serialised into JSON), then the client's `account_id`.

### Self-hosting: Basic auth

Operators of a self-hosted cluster can use the Basic-auth username/password configured on the server. The client then sends `Authorization: Basic ...` plus `X-Peer: cmd`; this satisfies the `admin`-only endpoints (accounts, cluster, `rotate_secret`).

```python
from scheduler0 import NewBasicAuthClient

client = NewBasicAuthClient("https://your-scheduler0-instance.com", "v1", "username", "password")
```

### Credential scopes

Each credential carries `scopes`, a non-empty subset of `read`, `write`, `execute`, `admin` (`admin` satisfies everything). A missing scope yields `403 credential missing required scope: <scope>`; an expired credential yields `401`.

| Scope | Grants |
|-------|--------|
| `read` | All `GET`s: jobs, projects, credentials, executors, executions/*, async-tasks/{id}, features, ai/settings, ai/models, ai/prompt-requests, local-executors/{id}/jobs |
| `write` | `POST`/`PUT`/`DELETE` on jobs, projects, credentials, executors, ai/settings; `POST /local-executors` |
| `execute` | ai/prompt, ai/prompt/classify, ai/schedule, ai/suggestions/*, executions/cleanup-old-logs, executors/{id}/test-invoke, local-executors/{id}/executions |
| `admin` | accounts/*, cluster/*, account/rotate-secret |

## Error handling

Any response with status `>= 400` raises `requests.HTTPError`; the message contains the response body and `e.response` is the original `requests.Response`. The server's error envelope is `{"success": false, "data": "<message>"}` (a few AI endpoints return `{"code", "message", "field"}` in `data`). Network failures raise the usual `requests` exceptions (`ConnectionError`, `Timeout`, ...).

```python
import requests

try:
    result = client.create_project(body)
except requests.HTTPError as e:
    status = e.response.status_code          # 400, 401, 403, 404, 409, 422, 429, ...
    detail = e.response.json().get("data")   # server error message
    print(status, detail)
```

A `2xx` response is never raised, so for methods that return the envelope check `result["success"]` (see the credentials note below for a case where this matters).

## Usage

All examples assume `client` was created as above.

### Projects

```python
from scheduler0.types import ProjectRequestBody, ProjectUpdateRequestBody, ProjectDeleteRequestBody

# GET /projects  -> data: {total, offset, limit, projects: [...]}
page = client.list_projects(limit=10, offset=0, order_by="date_created", order_by_direction="desc")
for project in page["data"]["projects"]:
    print(project["id"], project["name"])

# POST /projects (201). name must be unique per account.
created = client.create_project(ProjectRequestBody(
    name="My Project",
    description="Project description",
    created_by="user@example.com",
))
project_id = created["data"]["id"]

# GET /projects/{id}
project = client.get_project(str(project_id))

# PUT /projects/{id} - only description can change
client.update_project(str(project_id), ProjectUpdateRequestBody(
    description="Updated description",
    modified_by="user@example.com",
))

# DELETE /projects/{id} (204) - also deletes the project's jobs
client.delete_project(str(project_id), ProjectDeleteRequestBody(deleted_by="user@example.com"))
```

`order_by` accepts `id`, `name`, `description`, `date_created`, `account_id`; `order_by_direction` is `asc` or `desc`. `limit` above 100 is rejected with `429`.

### Jobs

`POST /jobs` always takes an **array** of jobs and is asynchronous: it returns `202` with `data` set to a request ID string. Poll `get_async_task(request_id)` to learn whether the jobs were created. `create_job(body)` is a convenience wrapper that sends a one-element array.

```python
from scheduler0.types import JobRequestBody, JobUpdateRequestBody, JobDeleteRequestBody

job = JobRequestBody(
    project_id=project_id,             # required
    timezone="UTC",                    # required (IANA name)
    created_by="user@example.com",     # required by the server (400 if missing)
    executor_id=456,                   # optional
    spec="0 30 * * * *",               # optional six-field cron (sec min hour dom month dow); empty = one-time job at start_date
    data='{"action": "process_data"}', # optional payload string
    start_date="2026-01-01T00:00:00Z", # optional RFC3339
    end_date="2026-12-31T23:59:59Z",   # optional RFC3339
    timezone_offset=0,                 # optional
    retry_max=3,                       # optional
    status="active",                   # optional: "active" | "inactive"
)

accepted = client.create_job(job)                 # 202
request_id = accepted["data"]                     # e.g. "b1c2..."

# Batch: several jobs in one request
accepted = client.batch_create_jobs([job, job])
request_id = accepted["data"]

# GET /async-tasks/{id} - blocks until the task finishes if it is still running
task = client.get_async_task(request_id)
state = task["data"]["state"]   # 0 not started, 1 in progress, 2 success, 3 failed
output = task["data"]["output"] # JSON-encoded created jobs on success, error text on failure

# GET /jobs -> data: {total, offset, limit, jobs: [...]}
page = client.list_jobs(project_id=str(project_id), limit=10, offset=0,
                        order_by="date_created", order_by_direction="desc")

# GET /jobs/{id}
job_detail = client.get_job("42")

# PUT /jobs/{id} - modified_by is required; timezone/timezone_offset/executor_id keep their
# existing values when omitted
client.update_job("42", JobUpdateRequestBody(
    modified_by="user@example.com",
    spec="0 0 * * * *",
    status="inactive",
))

# DELETE /jobs/{id} (204)
client.delete_job("42", JobDeleteRequestBody(deleted_by="user@example.com"))
```

Job JSON fields: `id, projectId, spec, data, executorId, startDate, endDate, lastExecutionDate, timezone, timezoneOffset, retryMax, executionId, dateCreated, accountId, dateModified, createdBy, modifiedBy, deletedBy, status` (zero-valued fields are omitted).

### Executors

Executor `type` is one of `webhook_url`, `cloud_function`, `local`. `webhook_url` requires `webhook_url` and `webhook_method` (`GET`/`POST`/`PUT`/`DELETE`); `local` requires `command`. `cloud_api_key`, `cloud_api_secret` and `webhook_secret` are returned **only** in the create response and are `None`/absent on every read.

```python
from scheduler0.types import (
    ExecutorRequestBody, ExecutorUpdateRequestBody, ExecutorDeleteRequestBody,
    TestInvocationRequestBody, Job,
)

# GET /executors -> data: {total, offset, limit, executors: [...]} (keys omitted when empty)
page = client.list_executors(limit=10, offset=0, order_by="date_created", order_by_direction="desc")

# POST /executors (201). description/tags are used by schedule_from_prompt to match executors.
created = client.create_executor(ExecutorRequestBody(
    name="webhook-executor",
    type="webhook_url",
    webhook_url="https://example.com/webhook",
    webhook_method="POST",
    webhook_secret="secret-key",
    description="Sends transactional email to customers",
    tags=["email", "notifications"],
    payload_aggregation=False,   # True = one call for all jobs firing at the same time
    created_by="user@example.com",
))
executor_id = created["data"]["id"]

client.create_executor(ExecutorRequestBody(
    name="cloud-function-executor",
    type="cloud_function",
    cloud_provider="aws",
    region="us-west-1",
    cloud_resource_url="https://example.com/function",
    cloud_api_key="api-key",
    cloud_api_secret="api-secret",
    created_by="user@example.com",
))

# GET /executors/{id}
executor = client.get_executor(str(executor_id))

# PUT /executors/{id} - modified_by required
client.update_executor(str(executor_id), ExecutorUpdateRequestBody(
    name="updated-executor",
    type="webhook_url",
    webhook_url="https://example.com/webhook-v2",
    webhook_method="POST",
    modified_by="user@example.com",
))

# POST /executors/{id}/test-invoke - fires a synthetic job now, no side effects.
# Body is optional. Local executors cannot be test-invoked (400).
result = client.test_invoke_executor(str(executor_id), TestInvocationRequestBody(
    job=Job(spec="0 0 2 * * *", data='{"action": "process_data"}', timezone="UTC", retry_max=2),
    age="24h",                              # Go duration: how old the synthetic job looks
    execution_time="2026-01-15T02:00:00Z",  # optional RFC3339, defaults to now
))
# data: {test, executorId, executorType, success, error, startedAt, finishedAt, durationMs, payload}
print(result["data"]["success"], result["data"]["durationMs"])

# DELETE /executors/{id} (204)
client.delete_executor(str(executor_id), ExecutorDeleteRequestBody(deleted_by="user@example.com"))
```

`order_by` for executors and credentials accepts `id`, `date_created`, `date_modified`, `created_by`, `modified_by`, `deleted_by` (credentials also `expires_at`).

### Local executors

Local executors run a command on a machine you control. The `scheduler0` CLI normally drives the pull/report endpoints; the client exposes them for custom runners.

```python
from scheduler0.types import LocalExecutorRegisterRequest, LocalExecutionReport

# POST /local-executors (201) -> data: {"id": <executor id>}
reg = client.register_local_executor(LocalExecutorRegisterRequest(
    name="My Local Executor",
    command="/usr/local/bin/process-job.sh",
    working_dir="/home/deploy/app",      # optional
    created_by="user@example.com",       # required by the server
))
local_id = reg["data"]["id"]

# GET /local-executors/{id}/jobs -> data: [Job, ...] (active jobs assigned to this executor)
jobs = client.pull_local_executor_jobs(local_id)["data"]

# POST /local-executors/{id}/executions -> data: {"committed": n}
# state: 0 scheduled, 1 success, 2 failed
report = client.report_local_executions(local_id, [
    LocalExecutionReport(
        job_id=jobs[0]["id"],
        unique_id="exec-1",
        state=1,
        last_execution_time="2026-01-01T00:00:00Z",
        next_execution_time="2026-01-02T00:00:00Z",
    ),
])
print(report["data"]["committed"])
```

### Executions

```python
# GET /executions -> data: {total, offset, limit, executions: [...]}
# All filters are optional. Server default limit is 50 (the client sends 10 unless told otherwise).
page = client.list_executions(
    limit=50,
    offset=0,
    start_date="2026-01-01T00:00:00Z",    # RFC3339
    end_date="2026-12-31T23:59:59Z",
    project_id=project_id,
    job_id=42,
    state="failed",                       # "scheduled" | "success" | "failed"
    order_by="dateCreated",               # "dateCreated" | "lastExecutionDateTime" | "nextExecutionDateTime"
    order_direction="DESC",               # "ASC" | "DESC"
)
for execution in page["data"]["executions"]:
    # state: 0 scheduled, 1 success, 2 failed
    print(execution["jobId"], execution["state"], execution["lastExecutionDatetime"])

# GET /executions/analytics?startDate=YYYY-MM-DD&startTime=HH:MM[:SS]
# -> data: {accountId, timezone, startDate, startTime, endDate, endTime, points: [{date, time, scheduled, success, failed}]}
analytics = client.get_date_range_analytics(start_date="2026-01-01", start_time="00:00")

# GET /executions/totals -> data: {accountId, scheduled, success, failed}
totals = client.get_execution_totals(account_id=123)

# POST /executions/cleanup-old-logs (execute scope) -> data: {message}
# account_id must equal the X-Account-ID header; retention_months must be > 0.
client.cleanup_old_execution_logs(account_id="123", retention_months=6)
```

### Credentials

```python
from scheduler0.types import (
    CredentialCreateRequestBody, CredentialDeleteRequestBody, CredentialArchiveRequestBody,
)

# GET /credentials -> data: {total, offset, limit, credentials: [...]}
page = client.list_credentials(limit=10, offset=0, order_by="date_created", order_by_direction="desc")

# POST /credentials (201). scopes is required. Default expiry is 90 days; expires_in_seconds
# can only shorten it (the server clamps it). Granting "admin" needs an admin credential.
created = client.create_credential(CredentialCreateRequestBody(
    created_by="user@example.com",
    scopes=["read", "write", "execute"],
    expires_in_seconds=8 * 60 * 60,   # optional
))
api_key = created["data"]["apiKey"]
secret = created["data"]["plaintextSecret"]   # returned ONLY here; store it now

# GET /credentials/{id} (no secret in the response)
credential = client.get_credential("1")

# POST /credentials/{id}/archive (204)
client.archive_credential("1", CredentialArchiveRequestBody(archived_by="user@example.com"))

# DELETE /credentials/{id} (204)
client.delete_credential("1", CredentialDeleteRequestBody(deleted_by="user@example.com"))
```

`update_credential(id, CredentialUpdateRequestBody(modified_by=..., archived=...))` calls `PUT /credentials/{id}`. Only `archived` and `modified_by` can change; `api_key`, `api_secret`, `scopes` and `expires_at` are fixed at creation and the server rejects attempts to change the key or secret with `400`. An omitted `archived` is treated as `False` (un-archive). Servers older than the credential-update fix answer every call with HTTP 200 `{"success": false, "data": "api_key or api_secret cannot be empty"}` without raising, so check `success` if you target one. There is no rotate endpoint for a credential: create a new one, then archive the old one.

`rotate_secret(old_secret_key)` is a different, self-hosting-only operation (`POST /account/rotate-secret`, `admin` scope or Basic auth) that re-encrypts stored secrets after the operator changes the server `SecretKey`. It returns `data: {credentialsRotated, executorsRotated, aiSettingsRotated}`.

### AI: generate job configurations from a prompt

`POST /ai/prompt` (`execute` scope) returns job *configurations*; it does not create jobs. Counts against the account's monthly prompt quota (`429` when exhausted; `402` when platform AI credits are exhausted). A prompt the intent guardrail rejects raises `HTTPError` with status `422`. Returns a `PromptResult` dataclass.

```python
from scheduler0.types import PromptJobRequest, JobRequestBody

result = client.create_job_from_prompt(PromptJobRequest(
    prompt="Send weekly reports every Monday at 9 AM",
    purposes=["reporting"],                 # optional
    events=["weekly_cycle"],                # optional
    recipients=["team@example.com"],        # optional
    channels=["email"],                     # optional
    timezone="America/New_York",            # optional IANA name; invalid -> 400
    locale="en",                            # optional, default "en"
))

if result.classification:
    print(result.classification.decision, result.classification.reason)   # allow / clarify / reject

for provider in result.providers:
    print(provider.provider, provider.model, provider.total_tokens, provider.duration_ms)
    for cfg in provider.jobs:
        # cfg: kind (FOLLOW_UP|REMINDER|DIGEST), purpose, subject, next_run_at, recurrence, event,
        # delivery, cron_expression, channel, recipients, start_date, end_date, timezone, metadata
        client.create_job(JobRequestBody(
            project_id=project_id,
            timezone=cfg.timezone or "UTC",
            spec=cfg.cron_expression,
            start_date=cfg.start_date,
            end_date=cfg.end_date,
            created_by="ai-prompt",
        ))
```

### AI: classify a prompt only

`POST /ai/prompt/classify` runs the intent guardrail without invoking a model and consumes no prompt credits (it counts against the classify quota). Only `en*` locales are accepted (`400` otherwise); `503` if the classifier is not configured.

```python
from scheduler0.types import ClassifyPromptRequest

clf = client.classify_prompt(ClassifyPromptRequest(prompt="What is Kubernetes?"))
print(clf.decision, clf.reason)   # IntentClassification(text, decision, reason)
```

### AI: schedule jobs from a prompt

`POST /ai/schedule` (`execute` scope, `201`) runs the prompt pipeline, resolves or creates a project, picks an executor (pinned `executor_id`, the account's only executor, or the best `description`/`tags` match), and creates the jobs synchronously. Consumes one prompt credit. Raises `HTTPError` `422` when the guardrail rejects the prompt and `409` when there are no executors, no match, or no schedulable jobs.

```python
from scheduler0 import SchedulePromptRequest, ScheduleProjectInput

result = client.schedule_from_prompt(SchedulePromptRequest(
    prompt="Remind the sales team every Monday at 9am to review the pipeline",
    created_by="user@example.com",                       # required
    channels=["email"],
    project=ScheduleProjectInput(name="Sales reminders"), # or project_id=...
    # executor_id=3,                                      # pin an executor
))
print(result.project["id"], result.project_created)
print(result.executor["id"], result.executor_matched_by, result.executor_match_reason)  # pinned | only | llm
print(len(result.jobs), result.provider, result.model)
```

### AI: conversation suggestions

`POST /ai/suggestions/analyze` (`execute` scope). Request and response use **snake_case**. English only (`400` for other locales); counts against the classify quota.

```python
from scheduler0.types import AnalyzeSuggestionsRequest, SuggestionMessage, SuggestionOptions

result = client.analyze_suggestions(AnalyzeSuggestionsRequest(
    conversation_id="conv_123",
    messages=[
        SuggestionMessage(
            speaker="Victor",                          # string or SuggestionParticipant
            timestamp="2026-07-17T10:00:00-04:00",
            message="I'll send the proposal tomorrow.",
        ),
    ],
    options=SuggestionOptions(locale="en", default_timezone="America/Toronto"),
))
# AnalyzeSuggestionsResult: request_id, conversation_id, analyzed_at, suggestions, obligations, warnings, engine
for suggestion in result.suggestions:
    print(suggestion)
```

### AI: send-time suggestions

`POST /ai/suggestions/time` (`execute` scope). Deterministic time-zone math, no model, no credits. snake_case request; validation errors are `400` with `{code, message, field}` in `data`.

```python
from scheduler0.types import (
    SendTimeSuggestionsRequest, SendTimeParticipant, SendTimeMessage, SendTimeConstraints,
)

result = client.send_time_suggestions(SendTimeSuggestionsRequest(
    sender=SendTimeParticipant(id="user_123", timezone="America/Toronto"),
    recipients=[SendTimeParticipant(id="user_456", timezone="America/Los_Angeles", role="primary")],
    message=SendTimeMessage(priority="normal"),
    constraints=SendTimeConstraints(working_hours_only=True, avoid_weekends=True),
))
# SendTimeSuggestionsResult: request_id, reference_time, policy, engine, suggestions, search,
# rejected_summary, no_suggestion, send_now, warnings, metadata
for suggestion in result.suggestions:
    print(suggestion)
```

### AI: prompt-request log, models and settings

```python
from scheduler0 import AccountAISettings, ActiveModel

# GET /ai/prompt-requests -> PromptRequestsResult(requests, total, limit, offset)
log = client.list_prompt_requests(
    limit=25, offset=0,                 # limit is clamped to 100
    provider="openai", model=None, status="success",   # optional filters
    search="reminder",                  # full-text over the prompt
    start=None, end=None,               # RFC3339
    order="DESC",                       # "ASC", anything else = DESC
)
for req in log.requests:
    print(req.provider, req.model, req.total_tokens, req.estimated_cost_usd, req.status)

# GET /ai/models -> data: {provider: [{id, display_name, default}]}
catalog = client.get_ai_models()["data"]

# GET /ai/settings -> data: AccountAISettings (snake_case; keys masked)
settings = client.get_account_ai_settings("123")["data"]

# PUT /ai/settings -> data: {message}. Ordered active_models: primary first, then fallbacks.
client.upsert_account_ai_settings("123", AccountAISettings(
    active_models=[
        ActiveModel(provider="openai", model="gpt-4.1-mini"),
        ActiveModel(provider="anthropic", model="claude-sonnet-4-5"),
    ],
    openai_api_key="sk-...",
    anthropic_api_key="sk-ant-...",
    # bedrock_access_key_id, bedrock_secret_key, bedrock_region, openrouter_api_key
))
```

### Features

```python
# GET /features (read scope) -> data: [{id, name, dateCreated, dateModified}, ...]
features = client.list_features()["data"]
```

### Health

```python
# GET /healthcheck - no auth required
health = client.healthcheck()
print(health["data"]["leaderAddress"], health["data"]["leaderId"])
print(health["data"]["raftStats"]["state"])
```

### Accounts (self-hosting, `admin` scope or Basic auth)

For API-key callers the `{id}` in the path must equal `X-Account-ID` (`403` otherwise). The `account_id` argument is also sent as the `X-Account-ID` header.

```python
from scheduler0.types import AccountCreateRequestBody, AccountUpdateRequestBody, FeatureRequest

account = client.create_account(AccountCreateRequestBody(name="My Account"))          # POST /accounts (201)
account = client.get_account("123")                                                  # GET /accounts/{id}
account = client.update_account("123", AccountUpdateRequestBody(name="New Name"))    # PUT /accounts/{id}
# data: {id, name, features: [{accountId, featureId, feature}], dateCreated, dateModified}

client.add_feature_to_account("123", FeatureRequest(feature_id=1))        # PUT /accounts/{id}/feature (201) -> {featureId}
client.remove_feature_from_account("123", FeatureRequest(feature_id=1))   # DELETE /accounts/{id}/feature (204)
client.add_all_features_to_account("123")                                 # PUT /accounts/{id}/features/all -> {message}
client.remove_all_features_from_account("123")                            # DELETE /accounts/{id}/features/all -> {message}

count = client.get_account_execution_count("123")
# data: {id, accountId, executionCount, tokens, dateCreated, dateModified, nextResetDate}
client.increase_account_execution_count("123", 10000)                     # -> {newExecutionCount}

usage = client.get_ai_usage("123")
# data: {accountId, periodStart, nextResetDate, prompt: {limit, used, remaining}, classify: {...}, estimatedCostUsd}

client.get_account_tokens("123")                                          # -> {tokens}
client.add_account_tokens("123", 1000)                                    # amount > 0 -> {newBalance}

client.rotate_secret("<old-hex-secret-key>")                              # POST /account/rotate-secret
```

### Cluster, backup and restore (self-hosting, `admin` scope or Basic auth + `X-Peer`)

```python
client.list_cluster_nodes()                       # GET  /cluster/list-nodes -> data: [...]
client.add_self_to_cluster()                      # POST /cluster/add-self -> {status}
client.remove_self_from_cluster()                 # POST /cluster/remove-self
client.transfer_cluster_leadership()              # POST /cluster/transfer-leadership (leader only)
client.add_cluster_node("2", "127.0.0.1:7072", "http://127.0.0.1:9092")  # ?nodeId&nodeAddress&clientAddress
client.remove_cluster_node("2")                   # ?nodeId=
client.promote_cluster_node("2")                  # ?nodeId=
client.demote_cluster_node("2")                   # ?nodeId=
client.force_rebuild_cluster("1")                 # ?seedNodeId= (seed node only)
client.reset_raft()                               # clears local Raft state; the server process exits afterwards

client.dump_schedule_queue()                      # GET /cluster/dump/schedule-queue
client.dump_job_executions_cache()                # GET /cluster/dump/job-executions-cache
client.dump_job_queues()                          # GET /cluster/dump/job-queues
client.dump_job_queue_versions()                  # GET /cluster/dump/job-queue-versions

client.backup_database()                          # POST /cluster/backup  (202) -> {status, requestId}
client.restore_database("db-20260212-114810.db")  # POST /cluster/restore (202) -> {status, requestId}
```

## Constants

| Value | Meaning |
|-------|---------|
| Job `status` | `active`, `inactive` |
| Executor `type` | `webhook_url`, `cloud_function`, `local` |
| Executor `webhookMethod` | `GET`, `POST`, `PUT`, `DELETE` |
| Execution `state` (int) | `0` scheduled, `1` success, `2` failed; query filter uses `scheduled`/`success`/`failed` |
| Async task `state` (int) | `0` not started, `1` in progress, `2` success, `3` failed |
| Credential `scopes` | `read`, `write`, `execute`, `admin` |
| Prompt job `kind` | `FOLLOW_UP`, `REMINDER`, `DIGEST` |
| Intent `decision` | `allow`, `clarify`, `reject` |
| `executorMatchedBy` | `pinned`, `only`, `llm` |

Request bodies use camelCase on the wire (the client converts the dataclasses' snake_case fields), except `/ai/settings` and `/ai/suggestions/*`, which use snake_case end to end. Response payloads are returned as sent by the server.

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT. See [LICENSE](LICENSE).
