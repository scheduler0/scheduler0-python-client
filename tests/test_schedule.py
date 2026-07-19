"""
Tests for the schedule-from-prompt method (POST /ai/schedule).
"""

from unittest.mock import patch, Mock

from scheduler0.types import (
    IntentClassification,
    SchedulePromptRequest,
    ScheduleProjectInput,
    ScheduleResult,
)


class TestSchedule:
    """Test the schedule_from_prompt method."""

    @patch('scheduler0.client.Client._request')
    def test_schedule_from_prompt(self, mock_request, client):
        """schedule_from_prompt returns a ScheduleResult from the standard envelope."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "data": {
                "classification": {
                    "text": "remind the sales team every monday",
                    "decision": "allow",
                    "reason": "request_with_temporal_signal",
                },
                "project": {"id": 7, "name": "Sales reminders", "description": "auto"},
                "projectCreated": True,
                "executor": {"id": 3, "name": "Email sender", "description": "sends email", "tags": ["email"]},
                "executorMatchedBy": "llm",
                "executorMatchReason": "matches email channel",
                "jobs": [
                    {"id": 11, "projectId": 7, "executorId": 3, "spec": "0 9 * * 1", "timezone": "UTC", "status": "active"},
                ],
                "provider": "openai",
                "model": "gpt-4.1-mini",
            },
        }
        mock_request.return_value = mock_response

        body = SchedulePromptRequest(
            prompt="Remind the sales team every Monday at 9am",
            channels=["email"],
            created_by="victor",
            project=ScheduleProjectInput(name="Sales reminders"),
        )
        result = client.schedule_from_prompt(body)

        assert isinstance(result, ScheduleResult)
        assert result.project["id"] == 7
        assert result.project_created is True
        assert result.executor["id"] == 3
        assert result.executor_matched_by == "llm"
        assert result.executor_match_reason == "matches email channel"
        assert len(result.jobs) == 1
        assert result.jobs[0]["id"] == 11
        assert isinstance(result.classification, IntentClassification)
        assert result.classification.decision == "allow"
        assert result.provider == "openai"
        mock_request.assert_called_once_with(
            "POST", "/ai/schedule", body=body, params=None, account_id_override=None
        )
