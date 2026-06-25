"""
Tests for local executor methods.
"""

import pytest
from unittest.mock import patch
from scheduler0.types import LocalExecutorRegisterRequest, LocalExecutionReport


class TestLocalExecutors:
    """Test local executor methods."""

    @patch('scheduler0.client.Client._post')
    def test_register_local_executor(self, mock_post, client):
        """Test registering a local executor."""
        mock_post.return_value = {"success": True, "data": {"id": 42}}
        body = LocalExecutorRegisterRequest(
            name="My Local Executor",
            command="/usr/local/bin/process-job.sh",
            working_dir="/home/deploy/app",
            created_by="user@example.com",
        )
        result = client.register_local_executor(body)
        assert result["success"] is True
        assert result["data"]["id"] == 42
        mock_post.assert_called_once_with(
            "/local-executors", body, account_id_override=None
        )

    @patch('scheduler0.client.Client._get')
    def test_pull_local_executor_jobs(self, mock_get, client):
        """Test pulling jobs assigned to a local executor."""
        mock_get.return_value = {
            "success": True,
            "data": [{"id": 1, "executorId": 42, "spec": "* * * * *"}],
        }
        result = client.pull_local_executor_jobs(42)
        assert result["success"] is True
        assert len(result["data"]) == 1
        mock_get.assert_called_once_with(
            "/local-executors/42/jobs", params=None, account_id_override=None
        )

    @patch('scheduler0.client.Client._post')
    def test_report_local_executions(self, mock_post, client):
        """Test reporting a batch of local execution results."""
        mock_post.return_value = {"success": True, "data": {"committed": 2}}
        reports = [
            LocalExecutionReport(
                job_id=1,
                unique_id="exec-1",
                state=1,
                last_execution_time="2025-01-01T00:00:00Z",
                next_execution_time="2025-01-02T00:00:00Z",
                execution_version=5,
                job_queue_version=2,
            ),
            LocalExecutionReport(job_id=2, unique_id="exec-2", state=2),
        ]
        result = client.report_local_executions(42, reports)
        assert result["success"] is True
        assert result["data"]["committed"] == 2
        mock_post.assert_called_once_with(
            "/local-executors/42/executions", reports, account_id_override=None
        )

    @patch('scheduler0.client.Client._post')
    def test_report_local_executions_account_override(self, mock_post, client):
        """Test that the account ID override is forwarded."""
        mock_post.return_value = {"success": True, "data": {"committed": 1}}
        reports = [LocalExecutionReport(job_id=1, unique_id="exec-1", state=0)]
        client.report_local_executions(42, reports, account_id_override="456")
        mock_post.assert_called_once_with(
            "/local-executors/42/executions", reports, account_id_override="456"
        )

    def test_local_execution_report_serialization(self, client):
        """The report body must serialize to camelCase and drop None fields."""
        report = LocalExecutionReport(job_id=7, unique_id="exec-7", state=1)
        serialized = client._serialize_body(report)
        assert serialized == {"jobId": 7, "uniqueId": "exec-7", "state": 1}
