"""Tests for ImageToVideoTool"""

import pytest
from unittest.mock import Mock, patch
from tools.image_to_video import ImageToVideoTool


class TestImageToVideoTool:
    """Test cases for ImageToVideoTool"""

    @pytest.fixture
    def tool(self, mock_tool_runtime, mock_tool_session):
        """Create an ImageToVideoTool instance with mocked runtime"""
        tool = ImageToVideoTool(mock_tool_runtime, mock_tool_session)
        return tool

    def test_invoke_missing_credentials(self, mock_tool_session):
        """Test invoke with missing API key"""
        mock_runtime = Mock()
        mock_runtime.credentials = {}
        tool = ImageToVideoTool(mock_runtime, mock_tool_session)

        results = list(tool._invoke({}))
        assert len(results) == 1
        assert "API Key 未配置" in results[0].message

    @patch("tools.image_to_video.requests.post")
    @patch("tools.image_to_video.requests.get")
    @patch("tools.image_to_video.time.sleep")
    def test_invoke_success(
        self,
        mock_sleep,
        mock_get,
        mock_post,
        tool,
        image_to_video_params
    ):
        """Test successful video generation from image"""
        # Mock POST response (task creation)
        mock_post_response = Mock()
        mock_post_response.json.return_value = {"task_id": "test_task_456"}
        mock_post.return_value = mock_post_response

        # Mock GET response (task query - completed immediately)
        mock_get_response = Mock()
        mock_get_response.json.return_value = {
            "task_id": "test_task_456",
            "status": "completed",
            "video_url": "https://example.com/video_from_image.mp4",
            "duration": "5s"
        }
        mock_get.return_value = mock_get_response

        results = list(tool._invoke(image_to_video_params))

        assert len(results) == 2

        # First result - pending status
        pending_result = results[0]
        pending_data = eval(pending_result.message)
        assert pending_data["task_id"] == "test_task_456"
        assert pending_data["status"] == "pending"

        # Second result - completed status
        completed_result = results[1]
        completed_data = eval(completed_result.message)
        assert completed_data["task_id"] == "test_task_456"
        assert completed_data["status"] == "completed"
        assert completed_data["video_url"] == "https://example.com/video_from_image.mp4"

    @patch("tools.image_to_video.requests.post")
    @patch("tools.image_to_video.requests.get")
    @patch("tools.image_to_video.time.sleep")
    def test_invoke_timeout(
        self,
        mock_sleep,
        mock_get,
        mock_post,
        tool,
        image_to_video_params
    ):
        """Test video generation timeout"""
        # Mock POST response
        mock_post_response = Mock()
        mock_post_response.json.return_value = {"task_id": "test_task_456"}
        mock_post.return_value = mock_post_response

        # Mock GET response - always processing
        mock_get_response = Mock()
        mock_get_response.json.return_value = {
            "task_id": "test_task_456",
            "status": "processing"
        }
        mock_get.return_value = mock_get_response

        # Mock time to simulate timeout
        with patch("tools.image_to_video.time.time") as mock_time:
            mock_time.side_effect = [0, 30, 60, 301]  # Exceeds 300s timeout

        results = list(tool._invoke(image_to_video_params))

        assert len(results) == 2
        timeout_result = results[1]
        timeout_data = eval(timeout_result.message)
        assert timeout_data["status"] == "timeout"
        assert "超时" in timeout_data["error"]

    @patch("tools.image_to_video.requests.post")
    def test_create_video_task_with_image(self, mock_post, tool, image_to_video_params):
        """Test _create_video_task method includes image_url"""
        mock_response = Mock()
        mock_response.json.return_value = {"task_id": "test_task_789"}
        mock_post.return_value = mock_response

        task_id = tool._create_video_task("test_key", image_to_video_params)

        assert task_id == "test_task_789"
        mock_post.assert_called_once()

        # Verify image_url is in the request
        call_params = mock_post.call_args[1]["json"]
        assert "image_url" in call_params
        assert call_params["image_url"] == "https://example.com/image.jpg"

    @patch("tools.image_to_video.requests.get")
    @patch("tools.image_to_video.time.sleep")
    def test_poll_until_complete_completed(
        self,
        mock_sleep,
        mock_get,
        tool
    ):
        """Test _poll_until_complete returns on completed status"""
        mock_get_response = Mock()
        mock_get_response.json.return_value = {
            "status": "completed",
            "video_url": "https://example.com/video.mp4",
            "duration": "10s"
        }
        mock_get.return_value = mock_get_response

        result = tool._poll_until_complete("test_key", "task_123")

        assert result["status"] == "completed"
        assert result["video_url"] == "https://example.com/video.mp4"
        assert result["duration"] == "10s"


class TestImageToVideoToolEdgeCases:
    """Edge case tests for ImageToVideoTool"""

    @pytest.fixture
    def tool(self, mock_tool_runtime, mock_tool_session):
        """Create an ImageToVideoTool instance"""
        tool = ImageToVideoTool(mock_tool_runtime, mock_tool_session)
        return tool

    def test_invoke_missing_image_url(self, tool):
        """Test invoke without image_url parameter"""
        with patch("tools.image_to_video.requests.post") as mock_post, \
             patch("tools.image_to_video.requests.get") as mock_get, \
             patch("tools.image_to_video.time.sleep"):

            mock_post.return_value.json.return_value = {"task_id": "task_123"}
            mock_get.return_value.json.return_value = {
                "status": "completed",
                "video_url": "https://example.com/video.mp4"
            }

            # image_url is required but may be empty
            params = {
                "prompt": "test",
                "image_url": ""
            }
            results = list(tool._invoke(params))

            # Should still attempt to call API
            mock_post.assert_called_once()

    def test_invoke_with_10s_duration(self, tool):
        """Test invoke with 10 second duration"""
        with patch("tools.image_to_video.requests.post") as mock_post, \
             patch("tools.image_to_video.requests.get") as mock_get, \
             patch("tools.image_to_video.time.sleep"):

            mock_post.return_value.json.return_value = {"task_id": "task_123"}
            mock_get.return_value.json.return_value = {
                "status": "completed",
                "video_url": "https://example.com/video.mp4"
            }

            params = {
                "prompt": "test",
                "image_url": "https://example.com/image.jpg",
                "duration": "10s"
            }
            list(tool._invoke(params))

            call_params = mock_post.call_args[1]["json"]
            assert call_params["duration"] == "10s"

    def test_invoke_with_pro_model(self, tool):
        """Test invoke with sora-2-pro model"""
        with patch("tools.image_to_video.requests.post") as mock_post, \
             patch("tools.image_to_video.requests.get") as mock_get, \
             patch("tools.image_to_video.time.sleep"):

            mock_post.return_value.json.return_value = {"task_id": "task_123"}
            mock_get.return_value.json.return_value = {
                "status": "completed",
                "video_url": "https://example.com/video.mp4"
            }

            params = {
                "prompt": "test",
                "image_url": "https://example.com/image.jpg",
                "model": "sora-2-pro"
            }
            list(tool._invoke(params))

            call_params = mock_post.call_args[1]["json"]
            assert call_params["model"] == "sora-2-pro"


class TestImageToVideoToolParameters:
    """Parameter validation tests for ImageToVideoTool"""

    @pytest.fixture
    def tool(self, mock_tool_runtime, mock_tool_session):
        """Create an ImageToVideoTool instance"""
        tool = ImageToVideoTool(mock_tool_runtime, mock_tool_session)
        return tool

    @patch("tools.image_to_video.requests.post")
    @patch("tools.image_to_video.requests.get")
    @patch("tools.image_to_video.time.sleep")
    def test_all_parameters_in_request(
        self,
        mock_sleep,
        mock_get,
        mock_post,
        tool
    ):
        """Test all parameters are included in API request"""
        mock_post.return_value.json.return_value = {"task_id": "task_123"}
        mock_get.return_value.json.return_value = {
            "status": "completed",
            "video_url": "https://example.com/video.mp4"
        }

        params = {
            "prompt": "A beautiful sunset over mountains",
            "image_url": "https://example.com/sunset.jpg",
            "model": "sora-2-pro",
            "duration": "10s"
        }
        list(tool._invoke(params))

        call_params = mock_post.call_args[1]["json"]
        assert call_params["prompt"] == "A beautiful sunset over mountains"
        assert call_params["image_url"] == "https://example.com/sunset.jpg"
        assert call_params["model"] == "sora-2-pro"
        assert call_params["duration"] == "10s"

        # Verify headers
        headers = mock_post.call_args[1]["headers"]
        assert "Authorization" in headers
        assert "Bearer test_key" in headers["Authorization"]
