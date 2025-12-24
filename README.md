<div align="center">
  <img src="logo.png" alt="Scheduler0 Logo" width="200"/>
</div>

# Scheduler0 Python Client

A Python client library for interacting with the [Scheduler0 API](https://scheduler0.com/api). This client provides a convenient way to manage accounts, credentials, executions, executors, projects, jobs, features, create jobs from AI prompts, and monitor the health of your Scheduler0 cluster.

## Features

- **Account Management** *(Self-hosted only)*
  - Create accounts
  - Get account details
  - Add/remove features from accounts
  - *Note: These APIs are for users running Scheduler0 in their own infrastructure who need granular control over team access and resource usage.*

- **Feature Management** *(Self-hosted only)*
  - List available features
  - *Note: These APIs are for users running Scheduler0 in their own infrastructure who need granular control over team access and resource usage.*

- **Credentials Management**
  - List credentials with pagination and ordering
  - Create new credentials
  - Get credential details
  - Update credentials
  - Delete credentials
  - Archive credentials

- **Executions Management**
  - List job executions with date filtering
  - Filter by project ID and job ID
  - View execution details and logs

- **Executors Management**
  - List executors with pagination and ordering
  - Create new executors (webhook, cloud function, container)
  - Get executor details
  - Update executors
  - Delete executors

- **Projects Management**
  - List projects with pagination
  - Create new projects
  - Get project details
  - Update projects
  - Delete projects

- **Jobs Management**
  - List jobs with pagination and ordering
  - Create new jobs with comprehensive scheduling options
  - Batch create multiple jobs in a single request
  - Get job details
  - Update jobs
  - Delete jobs

- **AI-Powered Job Creation**
  - Create job configurations from natural language prompts
  - AI generates cron expressions, scheduling, and job metadata
  - Supports purposes, events, recipients, and channels

- **Async Tasks Management** *(Self-hosted only)*
  - Get async task status by request ID
  - *Note: These APIs are for users running Scheduler0 in their own infrastructure who need granular control over team access and resource usage.*

- **Health Monitoring**
  - Check cluster health
  - View raft statistics
  - Monitor leader status

## Installation

```bash
pip install scheduler0-python-client
```

Or install from source:

```bash
git clone https://github.com/scheduler0/scheduler0-python-client.git
cd scheduler0-python-client
pip install .
```

## API Documentation

- **OpenAPI Specification**: [openapi.json](https://api-reference.scheduler0.com) - Complete API specification

## Authentication

The Scheduler0 Python client supports multiple authentication methods:

### 1. API Key + Secret Authentication (Default)
Most endpoints require API Key and Secret authentication with an Account ID:

```python
from scheduler0 import NewAPIClientWithAccount

client = NewAPIClientWithAccount(
    base_url="http://localhost:7070",  # Base URL
    version="v1",                       # API Version
    api_key="your-api-key",             # API Key
    api_secret="your-api-secret",       # API Secret
    account_id="123",                   # Account ID
)
```

### 2. Basic Authentication (Peer Communication)
For peer-to-peer communication:

```python
from scheduler0 import NewBasicAuthClient

client = NewBasicAuthClient(
    base_url="http://localhost:7070",  # Base URL
    version="v1",                      # API Version
    username="username",               # Username
    password="password",               # Password
)
```

### 3. Flexible Options Pattern
For more flexibility, use the options pattern:

```python
from scheduler0 import NewClient

client = NewClient(
    base_url="http://localhost:7070",
    version="v1",
    api_key="api-key",
    api_secret="api-secret",
    account_id="123",
)
```

## Usage

> **Note for Self-hosted Users**: Account Management, Feature Management, and Async Tasks Management APIs are designed for users running Scheduler0 in their own infrastructure who need granular control over team access and resource usage. If you're using Scheduler0's hosted service, these endpoints may not be available or may work differently.

### Managing Accounts

> **Note**: Account Management is designed for self-hosted deployments where you need granular control over team access and resource usage.

```python
from scheduler0 import NewAPIClientWithAccount
from scheduler0.types import AccountCreateRequestBody, FeatureRequest

client = NewAPIClientWithAccount(
    "http://localhost:7070", "v1", "api-key", "api-secret", "123"
)

# Create a new account
account_body = AccountCreateRequestBody(name="My Account")
result = client.create_account(account_body)

# Get account details
account = client.get_account("account-id")

# Add feature to account
feature = FeatureRequest(feature_id=1)
result = client.add_feature_to_account("account-id", feature)

# Remove feature from account
client.remove_feature_from_account("account-id", feature)
```

### Managing Features

> **Note**: Feature Management is designed for self-hosted deployments where you need granular control over team access and resource usage.

```python
# List all available features
features = client.list_features()
```

### Managing Credentials

```python
from scheduler0.types import (
    CredentialCreateRequestBody,
    CredentialUpdateRequestBody,
    CredentialDeleteRequestBody,
    CredentialArchiveRequestBody,
)

# List credentials with pagination and ordering
credentials = client.list_credentials(
    limit=10,
    offset=0,
    order_by="date_created",
    order_by_direction="desc",
)

# Create a new credential
credential_body = CredentialCreateRequestBody(created_by="user@example.com")
credential = client.create_credential(credential_body)

# Get a specific credential
credential = client.get_credential("credential-id")

# Update a credential
update_body = CredentialUpdateRequestBody(
    modified_by="user@example.com",
    archived=False,
)
credential = client.update_credential("credential-id", update_body)

# Delete a credential
delete_body = CredentialDeleteRequestBody(deleted_by="user@example.com")
client.delete_credential("credential-id", delete_body)

# Archive a credential
archive_body = CredentialArchiveRequestBody(archived_by="user@example.com")
client.archive_credential("credential-id", archive_body)
```

### Managing Executions

```python
# List executions with date filtering
executions = client.list_executions(
    start_date="2024-01-01T00:00:00Z",  # Required: Start date (RFC3339 format)
    end_date="2024-12-31T23:59:59Z",    # Required: End date (RFC3339 format)
    project_id=0,                       # Optional: Project ID (0 for all)
    job_id=0,                           # Optional: Job ID (0 for all)
    limit=10,                           # Required: Maximum number of items
    offset=0,                           # Required: Number of items to skip
)
```

### Managing Executors

```python
from scheduler0.types import (
    ExecutorRequestBody,
    ExecutorUpdateRequestBody,
    ExecutorDeleteRequestBody,
)

# List executors with pagination and ordering
executors = client.list_executors(
    limit=10,
    offset=0,
    order_by="date_created",
    order_by_direction="desc",
)

# Create a webhook executor
executor = ExecutorRequestBody(
    name="webhook-executor",
    type="webhook_url",
    webhook_url="https://example.com/webhook",
    webhook_method="POST",
    webhook_secret="secret-key",
    created_by="user@example.com",
)
result = client.create_executor(executor)

# Create a cloud function executor
executor = ExecutorRequestBody(
    name="cloud-function-executor",
    type="cloud_function",
    region="us-west-1",
    cloud_provider="aws",
    cloud_resource_url="https://example.com/function",
    cloud_api_key="api-key",
    cloud_api_secret="api-secret",
    created_by="user@example.com",
)
result = client.create_executor(executor)

# Get a specific executor
executor = client.get_executor("executor-id")

# Update an executor
update = ExecutorUpdateRequestBody(
    name="updated-executor",
    type="webhook_url",
    modified_by="user@example.com",
    # ... other fields
)
result = client.update_executor("executor-id", update)

# Delete an executor
delete_body = ExecutorDeleteRequestBody(deleted_by="user@example.com")
client.delete_executor("executor-id", delete_body)
```

### Managing Projects

```python
from scheduler0.types import (
    ProjectRequestBody,
    ProjectUpdateRequestBody,
    ProjectDeleteRequestBody,
)

# List projects with pagination and ordering
projects = client.list_projects(
    limit=10,
    offset=0,
    order_by="date_created",
    order_by_direction="desc",
)

# Create a new project
project = ProjectRequestBody(
    name="My Project",
    description="Project description",
    created_by="user@example.com",
)
result = client.create_project(project)

# Get a specific project
project = client.get_project("project-id")

# Update a project
update = ProjectUpdateRequestBody(
    description="Updated description",
    modified_by="user@example.com",
)
result = client.update_project("project-id", update)

# Delete a project
delete_body = ProjectDeleteRequestBody(deleted_by="user@example.com")
client.delete_project("project-id", delete_body)
```

### Managing Jobs

```python
from scheduler0.types import (
    JobRequestBody,
    JobUpdateRequestBody,
    JobDeleteRequestBody,
)

# List jobs with pagination and ordering
jobs = client.list_jobs(
    project_id="",              # Optional: Project ID to filter by (empty string for all)
    limit=10,
    offset=0,
    order_by="date_created",
    order_by_direction="desc",
)

# Create a single job
job = JobRequestBody(
    project_id=123,                    # Required
    timezone="UTC",                    # Required
    executor_id=456,                   # Optional
    data="job payload data",           # Optional
    spec="0 30 * * * *",              # Optional
    start_date="2024-01-01T00:00:00Z", # Optional
    end_date="2024-12-31T23:59:59Z",   # Optional
    timezone_offset=0,                 # Optional
    retry_max=3,                       # Optional
    status="active",                   # Optional
    created_by="user@example.com",     # Optional
)
result = client.create_job(job)

# Create multiple jobs in a single batch request
jobs = [
    JobRequestBody(
        project_id=123,
        timezone="UTC",
        data="job 1 payload",
        spec="0 30 * * * *",
        start_date="2024-01-01T00:00:00Z",
        retry_max=3,
        created_by="user@example.com",
    ),
    JobRequestBody(
        project_id=123,
        timezone="UTC",
        data="job 2 payload",
        spec="0 0 * * * *",
        start_date="2024-01-01T00:00:00Z",
        retry_max=5,
        created_by="user@example.com",
    ),
]
batch_result = client.batch_create_jobs(jobs)

# Get a specific job
job = client.get_job("job-id")

# Update a job
update = JobUpdateRequestBody(
    data="updated payload",
    spec="0 0 * * * *",
    status="inactive",
    modified_by="user@example.com",
)
result = client.update_job("job-id", update)

# Delete a job
delete_body = JobDeleteRequestBody(deleted_by="user@example.com")
client.delete_job("job-id", delete_body)
```

### AI-Powered Job Creation

Create job configurations from natural language prompts using AI:

```python
from scheduler0.types import PromptJobRequest, JobRequestBody

# Create job configurations from a natural language prompt
prompt_request = PromptJobRequest(
    prompt="Send weekly reports every Monday at 9 AM",
    purposes=["reporting", "communication"],
    events=["weekly_cycle"],
    recipients=["team@example.com", "manager@example.com"],
    channels=["email"],
    timezone="America/New_York",
)

# Generate job configurations from the prompt
# Note: This endpoint requires credits and validates credentials
job_configs = client.create_job_from_prompt(prompt_request)

# job_configs is a list of PromptJobResponse dictionaries
for config in job_configs:
    print(f"Kind: {config.get('kind')}")
    print(f"Cron Expression: {config.get('cronExpression')}")
    if config.get("nextRunAt"):
        print(f"Next Run At: {config.get('nextRunAt')}")
    print(f"Recipients: {config.get('recipients')}")
    
    # Use the generated configuration to create actual jobs
    job = JobRequestBody(
        project_id=123,
        timezone=config.get("timezone", "UTC"),
        spec=config.get("cronExpression"),
        created_by="ai-prompt",
    )
    
    # Set optional fields if available
    if config.get("startDate"):
        job.start_date = config.get("startDate")
    if config.get("endDate"):
        job.end_date = config.get("endDate")
    if config.get("subject"):
        import json
        job.data = json.dumps({
            "subject": config.get("subject"),
            "recipients": config.get("recipients", []),
        })
    
    result = client.create_job(job)
    print(f"Job created with request ID: {result.get('data')}")
```

**Note**: The AI prompt endpoint requires:
- Valid API credentials (API Key + Secret)
- Account ID header
- Sufficient credits (1 credit per prompt execution)

### Managing Async Tasks

> **Note**: Async Tasks Management is designed for self-hosted deployments where you need granular control over team access and resource usage.

```python
# Get async task status
task = client.get_async_task("request-id")
```

### Health Monitoring

```python
# Check cluster health (no authentication required)
health = client.healthcheck()
print(f"Leader: {health['data']['leaderAddress']}")
print(f"Raft State: {health['data']['raftStats']['state']}")
```

## Data Types

### Job Status
- `"active"` - Job is active and will be executed
- `"inactive"` - Job is inactive and will not be executed

### Executor Types
- `"webhook_url"` - HTTP webhook executor
- `"cloud_function"` - Cloud function executor
- `"container"` - Container executor

### Webhook Methods
- `"GET"`, `"POST"`, `"PUT"`, `"DELETE"`

### Job Creation Behavior
- **Single Job Creation**: `create_job()` internally uses batch creation with a single job
- **Batch Job Creation**: `batch_create_jobs()` allows creating multiple jobs in one API call
- **Backend API**: The `/api/v1/jobs` POST endpoint expects an array of jobs for batch processing
- **Response Format**: Job creation returns a dict with HTTP 202 Accepted status and a `data` field containing the request ID (string) for async task tracking
- **Async Tracking**: Use the request ID with `get_async_task()` to track job creation status

## Error Handling

The client raises `requests.HTTPError` for API errors. Check the error message for details:

```python
import requests

try:
    result = client.create_job(job)
except requests.HTTPError as e:
    if e.response.status_code == 400:
        # Handle bad request
        print(f"Bad request: {e}")
    elif e.response.status_code == 401:
        # Handle unauthorized
        print(f"Unauthorized: {e}")
    elif e.response.status_code == 403:
        # Handle forbidden
        print(f"Forbidden: {e}")
    elif e.response.status_code == 404:
        # Handle not found
        print(f"Not found: {e}")
    else:
        print(f"Error: {e}")
```

## Account ID Requirements

Most endpoints require the `X-Account-ID` header. The following endpoints require account ID:
- `/api/v1/jobs/*`
- `/api/v1/projects/*`
- `/api/v1/credentials/*`
- `/api/v1/executors/*`
- `/api/v1/async-tasks/*`
- `/api/v1/executions`
- `/api/v1/prompt` (AI prompt endpoint)

Account endpoints (`/api/v1/accounts/*`) and features (`/api/v1/features`) do not require account ID.

### Per-Request Account ID Override

You can override the Account ID set during client initialization on a per-request basis:

```python
# Override Account ID for a specific request
projects = client.list_projects(
    limit=10,
    offset=0,
    account_id_override="456",  # Overrides the client's default Account ID
)
```

For other methods, the Account ID can be set in the request body's `account_id` field (which is excluded from JSON serialization but used for the `X-Account-ID` header).

## Credits and AI Features

The AI prompt endpoint (`/api/v1/prompt`) requires:
- **Credits**: 1 credit per prompt execution
- **Authentication**: Valid API Key + Secret credentials
- **Account ID**: Required header for credit deduction

Credits are automatically deducted when the prompt is successfully processed. If the prompt processing fails after credit deduction, credits are not refunded.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run tests with coverage
pytest --cov=scheduler0 --cov-report=html

# Run specific test file
pytest tests/test_client.py

# Run with verbose output
pytest -v
```

### CI/CD

This project uses GitHub Actions for continuous integration. Tests are automatically run on:
- Push to `main`, `master`, or `develop` branches
- Pull requests to `main`, `master`, or `develop` branches

The CI pipeline includes:
- **Tests**: Runs pytest on multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12) across Ubuntu, macOS, and Windows
- **Build**: Builds the package and validates it can be distributed
- **Lint**: Checks code formatting, import sorting, and basic type checking

Package builds are automatically published to PyPI when tags starting with `v` are pushed (e.g., `v1.0.0`).

### Test Structure

The test suite includes:
- **test_client.py**: Core client functionality, authentication, request building, error handling
- **test_accounts.py**: Account management methods
- **test_credentials.py**: Credential management methods
- **test_jobs.py**: Job management methods (single and batch)
- **test_projects.py**: Project management methods
- **test_executors.py**: Executor management methods
- **test_executions.py**: Execution listing methods
- **test_features.py**: Feature listing methods
- **test_async_tasks.py**: Async task status methods
- **test_healthcheck.py**: Health monitoring methods
- **test_prompt.py**: AI-powered job creation methods
- **test_types.py**: Type definition validation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

