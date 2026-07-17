"""
Tests for conversation suggestions analysis.
"""

from unittest.mock import Mock, patch

from scheduler0.types import (
    AnalyzeSuggestionsRequest,
    AnalyzeSuggestionsResult,
    SuggestionMessage,
    SuggestionOptions,
    SendTimeConstraints,
    SendTimeMessage,
    SendTimeParticipant,
    SendTimeSuggestionsRequest,
    SendTimeSuggestionsResult,
)


class TestSuggestions:
    """Test the analyze_suggestions method."""

    @patch("scheduler0.client.requests.Session.request")
    def test_analyze_suggestions(self, mock_request, client):
        """analyze_suggestions posts snake_case JSON and parses the envelope."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {
                "request_id": "req_1",
                "conversation_id": "conv_123",
                "suggestions": [
                    {"id": "sug_001", "type": "COMMITMENT", "status": "OPEN", "confidence": 0.95}
                ],
                "obligations": [
                    {"id": "obl_001", "status": "OPEN", "suggestion_id": "sug_001"}
                ],
                "warnings": [],
                "engine": {"engine_version": "1.0.0"},
            },
        }
        mock_request.return_value = mock_response

        body = AnalyzeSuggestionsRequest(
            conversation_id="conv_123",
            messages=[
                SuggestionMessage(
                    speaker="Victor",
                    timestamp="2026-07-17T10:00:00-04:00",
                    message="I'll send the proposal tomorrow.",
                )
            ],
            options=SuggestionOptions(locale="en", default_timezone="America/Toronto"),
        )
        result = client.analyze_suggestions(body)

        assert isinstance(result, AnalyzeSuggestionsResult)
        assert result.conversation_id == "conv_123"
        assert len(result.suggestions) == 1
        assert result.suggestions[0]["type"] == "COMMITMENT"
        assert len(result.obligations) == 1

        # The request targets the analyze endpoint and preserves snake_case keys.
        _, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v1/suggestions/analyze")
        assert kwargs["method"] == "POST"
        payload = kwargs["json"]
        assert payload["conversation_id"] == "conv_123"
        assert payload["options"]["default_timezone"] == "America/Toronto"
        # None-valued optional fields are stripped.
        assert "reference_time" not in payload["options"]


class TestSendTimeSuggestions:
    """Test the send_time_suggestions method."""

    @patch("scheduler0.client.requests.Session.request")
    def test_send_time_suggestions(self, mock_request, client):
        """send_time_suggestions posts snake_case JSON and parses the envelope."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {
                "request_id": "req_1",
                "reference_time": "2026-07-17T17:45:00-04:00",
                "policy": {"id": "default_send_time", "version": "1.0.0"},
                "engine": {"version": "1.0.0"},
                "suggestions": [
                    {
                        "id": "sts_001",
                        "send_at": "2026-07-20T12:00:00-04:00",
                        "label": "Monday morning",
                        "score": 0.94,
                        "rank": 1,
                    }
                ],
                "search": {"candidates_generated": 143, "candidates_scored": 16},
                "warnings": [],
            },
        }
        mock_request.return_value = mock_response

        body = SendTimeSuggestionsRequest(
            sender=SendTimeParticipant(id="user_123", timezone="America/Toronto"),
            recipients=[
                SendTimeParticipant(
                    id="user_456", timezone="America/Los_Angeles", role="primary"
                )
            ],
            message=SendTimeMessage(priority="normal"),
            constraints=SendTimeConstraints(working_hours_only=True, avoid_weekends=True),
        )
        result = client.send_time_suggestions(body)

        assert isinstance(result, SendTimeSuggestionsResult)
        assert result.request_id == "req_1"
        assert result.reference_time == "2026-07-17T17:45:00-04:00"
        assert len(result.suggestions) == 1
        assert result.suggestions[0]["id"] == "sts_001"

        _, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v1/send-time-suggestions")
        assert kwargs["method"] == "POST"
        payload = kwargs["json"]
        assert payload["recipients"][0]["timezone"] == "America/Los_Angeles"
        assert payload["constraints"]["working_hours_only"] is True
        # None-valued optional fields are stripped.
        assert "preferences" not in payload
