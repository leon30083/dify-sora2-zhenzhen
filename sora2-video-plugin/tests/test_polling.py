"""Tests for polling behavior across tools"""

import pytest
import time
from unittest.mock import Mock, patch
from tools.text_to_video import TextToVideoTool
from tools.image_to_video import ImageToVideoTool


class TestPollingBehavior:
    """Test shared polling behavior"""

    @pytest.fixture
    def text_tool(self, mock_tool_runtime, mock_tool_session):
        tool = TextToVideoTool(mock_tool_runtime, mock_tool_session)
        return tool

    @pytest.fixture
    def image_tool(self, mock_tool_runtime, mock_tool_session):
        tool = ImageToVideoTool(mock_tool_runtime, mock_tool_session)
        return tool

    @patch("tools.text_to_video.time.sleep")
    @patch("tools.text_to_video.requests.get")
    def test_poll_interval_is_30_seconds(self, mock_get, mock_sleep, text_tool):
        """Test that polling interval is 30 seconds"""
        # First call: processing, second call: completed
        mock_get.side_effect = [
            Mock(json=lambda: {"status": "processing"}),
            Mock(json=lambda: {"status": "completed", "video_url": "https://example.com/video.mp4"})
        ]

        text_tool._poll_until_complete("test_key", "task_123", poll_interval=30)

        # Verify sleep was called with 30 seconds
        mock_sleep.assert_called_with(30)

    @patch("tools.text_to_video.time.sleep")
    @patch("tools.text_to_video.requests.get")
    def test_custom_poll_interval(self, mock_get, mock_sleep, text_tool):
        """Test custom polling interval"""
        mock_get.side_effect = [
            Mock(json=lambda: {"status": "processing"}),
            Mock(json=lambda: {"status": "completed", "video_url": "https://example.com/video.mp4"})
        ]

        text_tool._poll_until_complete("test_key", "task_123", poll_interval=15)

        # Verify sleep was called with custom interval
        mock_sleep.assert_called_with(15)

    @patch("tools.text_to_video.time.sleep")
    @patch("tools.text_to_video.requests.get")
    @patch("tools.text_to_video.time.time")
    def test_timeout_after_300_seconds(self, mock_time, mock_get, mock_sleep, text_tool):
        """Test that timeout occurs after 300 seconds (5 minutes)"""
        # Simulate time progression
        mock_time.side_effect = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 301]

        # Always return processing status
        mock_get.return_value = Mock(json=lambda: {"status": "processing"})

        with pytest.raises(TimeoutError) as exc_info:
            text_tool._poll_until_complete("test_key", "task_123", timeout=300)

        assert "超时" in str(exc_info.value)

    @patch("tools.text_to_video.time.sleep")
    @patch("tools.text_to_video.requests.get")
    def test_max_retries_behavior(self, mock_get, mock_sleep, text_tool):
        """Test that polling continues until completion (no artificial retry limit)"""
        # Simulate 5 processing states before completion
        processing_responses = [
            Mock(json=lambda: {"status": "processing"})
        ] * 5
        completed_response = Mock(json=lambda: {
            "status": "completed",
            "video_url": "https://example.com/video.mp4"
        })
        mock_get.side_effect = processing_responses + [completed_response]

        result = text_tool._poll_until_complete("test_key", "task_123")

        assert result["status"] == "completed"
        assert mock_sleep.call_count == 5

    @patch("tools.image_to_video.time.sleep")
    @patch("tools.image_to_video.requests.get")
    def test_image_tool_polling(self, mock_get, mock_sleep, image_tool):
        """Test that ImageToVideoTool uses same polling logic"""
        mock_get.side_effect = [
            Mock(json=lambda: {"status": "processing"}),
            Mock(json=lambda: {"status": "completed", "video_url": "https://example.com/video.mp4"})
        ]

        result = image_tool._poll_until_complete("test_key", "task_123")

        assert result["status"] == "completed"
        mock_sleep.assert_called_once_with(30)


class TestPollingEdgeCases:
    """Test edge cases in polling behavior"""

    @pytest.fixture
    def tool(self, mock_tool_runtime, mock_tool_session):
        tool = TextToVideoTool(mock_tool_runtime, mock_tool_session)
        return tool

    @patch("tools.text_to_video.time.sleep")
    @patch("tools.text_to_video.requests.get")
    def test_immediate_completion(self, mock_get, mock_sleep, tool):
        """Test when task completes immediately (no sleep needed)"""
        mock_get.return_value = Mock(json=lambda: {
            "status": "completed",
            "video_url": "https://example.com/video.mp4"
        })

        result = tool._poll_until_complete("test_key", "task_123")

        assert result["status"] == "completed"
        mock_sleep.assert_not_called()

    @patch("tools.text_to_video.time.sleep")
    @patch("tools.text_to_video.requests.get")
    def test_failed_status_stops_polling(self, mock_get, mock_sleep, tool):
        """Test that failed status immediately stops polling"""
        mock_get.return_value = Mock(json=lambda: {
            "status": "failed",
            "error": "Video generation failed"
        })

        with pytest.raises(Exception) as exc_info:
            tool._poll_until_complete("test_key", "task_123")

        assert "failed" in str(exc_info.value).lower()
        mock_sleep.assert_not_called()

    @patch("tools.text_to_video.time.sleep")
    @patch("tools.text_to_video.requests.get")
    @patch("tools.text_to_video.time.time")
    def test_timeout_during_processing(self, mock_time, mock_get, mock_sleep, tool):
        """Test timeout that occurs while task is still processing"""
        # Simulate time approaching and exceeding timeout
        mock_time.side_effect = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 301]

        mock_get.return_value = Mock(json=lambda: {"status": "processing"})

        with pytest.raises(TimeoutError):
            tool._poll_until_complete("test_key", "task_123", timeout=300)

        # Should have called sleep 9 times before timeout
        assert mock_sleep.call_count == 9


class TestConcurrentPolling:
    """Test concurrent polling scenarios"""

    @pytest.fixture
    def text_tool(self, mock_tool_runtime, mock_tool_session):
        tool = TextToVideoTool(mock_tool_runtime, mock_tool_session)
        return tool

    @pytest.fixture
    def image_tool(self, mock_tool_runtime, mock_tool_session):
        tool = ImageToVideoTool(mock_tool_runtime, mock_tool_session)
        return tool

    @patch("tools.image_to_video.time.sleep")
    @patch("tools.image_to_video.requests.get")
    @patch("tools.text_to_video.time.sleep")
    @patch("tools.text_to_video.requests.get")
    def test_both_tools_can_poll_simultaneously(
        self,
        text_mock_get,
        text_mock_sleep,
        image_mock_get,
        image_mock_sleep,
        text_tool,
        image_tool
    ):
        """Test that both tools can poll simultaneously without interference"""
        # Setup text tool polling
        text_mock_get.side_effect = [
            Mock(json=lambda: {"status": "processing"}),
            Mock(json=lambda: {"status": "completed", "video_url": "https://example.com/text.mp4"})
        ]

        # Setup image tool polling
        image_mock_get.side_effect = [
            Mock(json=lambda: {"status": "processing"}),
            Mock(json=lambda: {"status": "completed", "video_url": "https://example.com/image.mp4"})
        ]

        # Poll both tools
        text_result = text_tool._poll_until_complete("test_key", "task_1")
        image_result = image_tool._poll_until_complete("test_key", "task_2")

        assert text_result["status"] == "completed"
        assert image_result["status"] == "completed"
        assert text_mock_sleep.call_count == 1
        assert image_mock_sleep.call_count == 1
