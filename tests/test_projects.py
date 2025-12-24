"""
Tests for project management methods.
"""

import pytest
from unittest.mock import patch
from scheduler0.types import (
    ProjectRequestBody,
    ProjectUpdateRequestBody,
    ProjectDeleteRequestBody,
)


class TestProjects:
    """Test project management methods."""

    @patch('scheduler0.client.Client._get')
    def test_list_projects(self, mock_get, client):
        """Test listing projects."""
        mock_get.return_value = {
            "success": True,
            "data": {
                "total": 1,
                "projects": [{"id": 1, "name": "Test Project"}],
            },
        }
        result = client.list_projects(limit=10, offset=0)
        assert result["success"] is True
        call_args = mock_get.call_args
        assert call_args[1]["params"]["limit"] == "10"

    @patch('scheduler0.client.Client._post')
    def test_create_project(self, mock_post, client):
        """Test creating a project."""
        mock_post.return_value = {"success": True, "data": {"id": 1, "name": "Test Project"}}
        body = ProjectRequestBody(
            name="Test Project",
            description="Description",
            created_by="user@example.com",
        )
        result = client.create_project(body)
        assert result["success"] is True
        mock_post.assert_called_once_with("/projects", body, account_id_override=None)

    @patch('scheduler0.client.Client._get')
    def test_get_project(self, mock_get, client):
        """Test getting a project."""
        mock_get.return_value = {"success": True, "data": {"id": 1, "name": "Test Project"}}
        result = client.get_project("1")
        assert result["success"] is True
        mock_get.assert_called_once_with("/projects/1", params=None, account_id_override=None)

    @patch('scheduler0.client.Client._put')
    def test_update_project(self, mock_put, client):
        """Test updating a project."""
        mock_put.return_value = {"success": True, "data": {"id": 1}}
        body = ProjectUpdateRequestBody(
            description="Updated description",
            modified_by="user@example.com",
        )
        result = client.update_project("1", body)
        assert result["success"] is True
        mock_put.assert_called_once_with("/projects/1", body, account_id_override=None)

    @patch('scheduler0.client.Client._delete')
    def test_delete_project(self, mock_delete, client):
        """Test deleting a project."""
        body = ProjectDeleteRequestBody(deleted_by="user@example.com")
        client.delete_project("1", body)
        mock_delete.assert_called_once_with("/projects/1", body, account_id_override=None)

