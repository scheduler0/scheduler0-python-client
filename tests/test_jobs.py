"""
Tests for job management methods.
"""

import pytest
from unittest.mock import patch
from scheduler0.types import (
    JobRequestBody,
    JobUpdateRequestBody,
    JobDeleteRequestBody,
)


class TestJobs:
    """Test job management methods."""

    @patch('scheduler0.client.Client._get')
    def test_list_jobs(self, mock_get, client):
        """Test listing jobs."""
        mock_get.return_value = {
            "success": True,
            "data": {
                "total": 1,
                "jobs": [{"id": 1, "projectId": 123}],
            },
        }
        result = client.list_jobs(limit=10, offset=0)
        assert result["success"] is True
        call_args = mock_get.call_args
        assert call_args[1]["params"]["limit"] == "10"
        assert call_args[1]["params"]["offset"] == "0"

    @patch('scheduler0.client.Client._get')
    def test_list_jobs_with_project_filter(self, mock_get, client):
        """Test listing jobs with project filter."""
        client.list_jobs(project_id="123", limit=10, offset=0)
        call_args = mock_get.call_args
        assert call_args[1]["params"]["projectId"] == "123"

    @patch('scheduler0.client.Client._post')
    def test_create_job(self, mock_post, client):
        """Test creating a single job."""
        mock_post.return_value = {"success": True, "data": "request-id"}
        body = JobRequestBody(project_id=123, timezone="UTC", created_by="user")
        result = client.create_job(body)
        assert result["success"] is True
        # create_job wraps the body in a list and calls batch_create_jobs
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[0][0] == "/jobs"
        assert isinstance(call_args[0][1], list)
        assert len(call_args[0][1]) == 1

    @patch('scheduler0.client.Client._post')
    def test_batch_create_jobs(self, mock_post, client):
        """Test batch creating jobs."""
        mock_post.return_value = {"success": True, "data": "request-id"}
        jobs = [
            JobRequestBody(project_id=123, timezone="UTC", created_by="user"),
            JobRequestBody(project_id=456, timezone="UTC", created_by="user"),
        ]
        result = client.batch_create_jobs(jobs)
        assert result["success"] is True
        mock_post.assert_called_once_with("/jobs", jobs, account_id_override=None)

    @patch('scheduler0.client.Client._get')
    def test_get_job(self, mock_get, client):
        """Test getting a job."""
        mock_get.return_value = {"success": True, "data": {"id": 1, "projectId": 123}}
        result = client.get_job("1")
        assert result["success"] is True
        mock_get.assert_called_once_with("/jobs/1", params=None, account_id_override=None)

    @patch('scheduler0.client.Client._put')
    def test_update_job(self, mock_put, client):
        """Test updating a job."""
        mock_put.return_value = {"success": True, "data": {"id": 1}}
        body = JobUpdateRequestBody(
            modified_by="user@example.com",
            spec="0 0 * * * *",
            status="inactive",
        )
        result = client.update_job("1", body)
        assert result["success"] is True
        mock_put.assert_called_once_with("/jobs/1", body, account_id_override=None)

    @patch('scheduler0.client.Client._delete')
    def test_delete_job(self, mock_delete, client):
        """Test deleting a job."""
        body = JobDeleteRequestBody(deleted_by="user@example.com")
        client.delete_job("1", body)
        mock_delete.assert_called_once_with("/jobs/1", body, account_id_override=None)

