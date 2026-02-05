"""Tests for TextToVideoTool"""

import pytest
import time
from unittest.mock import Mock, patch, MagicMock
from tools.text_to_video import TextToVideoTool


class TestTextToVideoTool:
    """Test cases for TextToVideoTool"""

    @pytest.fixture
    def tool(self, mock_tool_runtime, mock_tool_session):
        """Create a TextToVideoTool instance with mocked runtime"""
        tool = TextToVideoTool(mock_tool_runtime, mock_tool_session)
        return tool

    def test_invoke_missing_credentials(self, mock_tool_session):
        """Test invoke with missing API key"""
        mock_runtime = Mock()
        mock_runtime.credentials = {}
        tool = TextToVideoTool(mock_runtime, mock_tool_session)

        results = list(tool._invoke({}))
        assert len(results) == 1
        assert "API Key 未配置" in results[0].message

    @patch("tools.text_to_video.requests.post")
    @patch("tools.text_to_video.requests.get")
    @patch("tools.text_to_video.time.sleep")
    def test_invoke_success(
        self,
        mock_sleep,
        mock_get,
        mock_post,
        tool,
        text_to_video_params,
        mock_video_task_response,
        mock_video_completed_response
    ):
        """Test successful video generation"""
        # Mock POST response (task creation)
        mock_post_response = Mock()
        mock_post_response.json.return_value = {"task_id": "test_task_123"}
        mock_post.return_value = mock_post_response

        # Mock GET response (task query - completed immediately)
        mock_get_response = Mock()
        mock_get_response.json.return_value = mock_video_completed_response
        mock_get.return_value = mock_get_response

        results = list(tool._invoke(text_to_video_params))

        assert len(results) == 2

        # First result - pending status
        pending_result = results[0]
        pending_data = eval(pending_result.message)
        assert pending_data["task_id"] == "test_task_123"
        assert pending_data["status"] == "pending"

        # Second result - completed status
        completed_result = results[1]
        completed_data = eval(completed_result.message)
        assert completed_data["task_id"] == "test_task_123"
        assert completed_data["status"] == "completed"
        assert completed_data["video_url"] == "https://example.com/video.mp4"

    @patch("tools.text_to_video.requests.post")
    @patch("tools.text_to_video.requests.get")
    @patch("tools.text_to_video.time.sleep")
    def test_invoke_timeout(
        self,
        mock_sleep,
        mock_get,
        mock_post,
        tool,
        text_to_video_params
    ):
        """Test video generation timeout"""
        # Mock POST response
        mock_post_response = Mock()
        mock_post_response.json.return_value = {"task_id": "test_task_123"}
        mock_post.return_value = mock_post_response

        # Mock GET response - always processing
        mock_get_response = Mock()
        mock_get_response.json.return_value = {
            "task_id": "test_task_123",
            "status": "processing"
        }
        mock_get.return_value = mock_get_response

        # Mock time to simulate timeout
        with patch("tools.text_to_video.time.time") as mock_time:
            mock_time.side_effect = [0, 30, 60, 301]  # Exceeds 300s timeout

        results = list(tool._invoke(text_to_video_params))

        assert len(results) == 2
        timeout_result = results[1]
        timeout_data = eval(timeout_result.message)
        assert timeout_data["status"] == "timeout"
        assert "超时" in timeout_data["error"]

    @patch("tools.text_to_video.requests.post")
    @patch("tools.text_to_video.requests.get")
    @patch("tools.text_to_video.time.sleep")
    def test_invoke_task_failed(
        self,
        mock_sleep,
        mock_get,
        mock_post,
        tool,
        text_to_video_params,
        mock_video_failed_response
    ):
        """Test video generation task failure"""
        # Mock POST response
        mock_post_response = Mock()
        mock_post_response.json.return_value = {"task_id": "test_task_123"}
        mock_post.return_value = mock_post_response

        # Mock GET response - task failed
        mock_get_response = Mock()
        mock_get_response.json.return_value = mock_video_failed_response
        mock_get.return_value = mock_get_response

        results = list(tool._invoke(text_to_video_params))

        assert len(results) == 2
        failed_result = results[1]
        failed_data = eval(failed_result.message)
        assert failed_data["status"] == "failed"
        assert "failed" in failed_data["error"].lower()

    @patch("tools.text_to_video.requests.post")
    def test_create_video_task(self, mock_post, tool, text_to_video_params):
        """Test _create_video_task method"""
        mock_response = Mock()
        mock_response.json.return_value = {"task_id": "test_task_456"}
        mock_post.return_value = mock_response

        task_id = tool._create_video_task("test_key", text_to_video_params)

        assert task_id == "test_task_456"
        mock_post.assert_called_once()

    @patch("tools.text_to_video.requests.get")
    @patch("tools.text_to_video.time.sleep")
    def test_poll_until_complete_with_retries(
        self,
        mock_sleep,
        mock_get,
        tool
    ):
        """Test _poll_until_complete with multiple polling attempts"""
        # First call: processing, second call: completed
        mock_get.side_effect = [
            Mock(json=lambda: {"status": "processing"}),
            Mock(json=lambda: {
                "status": "completed",
                "video_url": "https://example.com/video.mp4"
            })
        ]

        result = tool._poll_until_complete("test_key", "task_123")

        assert result["status"] == "completed"
        assert result["video_url"] == "https://example.com/video.mp4"
        assert mock_sleep.call_count == 1

    def test_query_task(self, tool):
        """Test _query_task method"""
        with patch("tools.text_to_video.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "task_id": "task_123",
                "status": "processing"
            }
            mock_get.return_value = mock_response

            result = tool._query_task(
                "https://gpt-best.apifox.cn",
                {"Authorization": "Bearer test_key"},
                "task_123"
            )

            assert result["status"] == "processing"
            mock_get.assert_called_once()


class TestTextToVideoToolEdgeCases:
    """Edge case tests for TextToVideoTool"""

    @pytest.fixture
    def tool(self, mock_tool_runtime, mock_tool_session):
        """Create a TextToVideoTool instance"""
        tool = TextToVideoTool(mock_tool_runtime, mock_tool_session)
        return tool

    def test_invoke_with_default_parameters(self, tool):
        """Test invoke with only required parameter (prompt)"""
        with patch("tools.text_to_video.requests.post") as mock_post, \
             patch("tools.text_to_video.requests.get") as mock_get, \
             patch("tools.text_to_video.time.sleep"):

            mock_post.return_value.json.return_value = {"task_id": "task_123"}
            mock_get.return_value.json.return_value = {
                "status": "completed",
                "video_url": "https://example.com/video.mp4"
            }

            results = list(tool._invoke({"prompt": "test prompt"}))

            # Verify default values are used
            mock_post.assert_called_once()
            call_params = mock_post.call_args[1]["json"]
            assert call_params["model"] == "sora-2"
            assert call_params["duration"] == "5s"
            assert call_params["aspect_ratio"] == "16:9"

    def test_invoke_with_sora_pro_model(self, tool):
        """Test invoke with sora-2-pro model"""
        with patch("tools.text_to_video.requests.post") as mock_post, \
             patch("tools.text_to_video.requests.get") as mock_get, \
             patch("tools.text_to_video.time.sleep"):

            mock_post.return_value.json.return_value = {"task_id": "task_123"}
            mock_get.return_value.json.return_value = {
                "status": "completed",
                "video_url": "https://example.com/video.mp4"
            }

            params = {
                "prompt": "test",
                "model": "sora-2-pro"
            }
            list(tool._invoke(params))

            call_params = mock_post.call_args[1]["json"]
            assert call_params["model"] == "sora-2-pro"
