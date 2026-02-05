import time
import requests
from typing import Dict, Any
from dify_plugin import Tool


class ImageToVideoTool(Tool):
    def _invoke(self, tool_parameters: dict) -> str:
        """图生视频工具 - 使用 Sora2 从图片生成视频"""
        api_key = self.runtime.credentials.get("api_key")
        if not api_key:
            yield self.create_text_message("API Key 未配置")
            return

        # 提取参数
        prompt = tool_parameters.get("prompt", "")
        images_input = tool_parameters.get("images", "")
        model = tool_parameters.get("model", "sora-2")
        duration = tool_parameters.get("duration", "10")
        aspect_ratio = tool_parameters.get("aspect_ratio", "16:9")

        # 将逗号分隔的图片URL转换为数组
        images = [img.strip() for img in images_input.split(",") if img.strip()]

        # 构建请求参数
        params = {
            "prompt": prompt,
            "model": model,
            "duration": duration,
            "aspect_ratio": aspect_ratio
        }

        # 只有当有图片时才添加 images 参数
        if images:
            params["images"] = images

        base_url = "https://ai.t8star.cn"
        headers = {"Authorization": f"Bearer {api_key}"}
        last_progress = ""
        start_time = time.time()
        task_id = None

        try:
            # 创建视频任务
            task_id = self._create_video_task(base_url, headers, params)

            # 返回初始状态
            yield self.create_json_message({
                "task_id": task_id,
                "status": "pending",
                "message": "视频生成任务已提交"
            })

            # 轮询直到完成
            timeout = 300  # 5分钟超时
            poll_interval = 30  # 30秒轮询间隔

            while True:
                if time.time() - start_time > timeout:
                    raise TimeoutError(f"任务超时: {task_id}")

                # 查询任务状态
                result = self._query_task(base_url, headers, task_id)
                status = result.get("status")
                progress = result.get("progress", "")

                # 发送进度更新（如果进度发生变化）
                if progress and progress != last_progress:
                    yield self.create_json_message({
                        "task_id": task_id,
                        "status": "processing",
                        "progress": progress
                    })
                    last_progress = progress

                # SUCCESS 表示完成，FAILURE 表示失败
                if status == "SUCCESS":
                    yield self.create_json_message({
                        "task_id": task_id,
                        "status": "completed",
                        "video_url": result.get("video_url", ""),
                        "duration": duration
                    })
                    break
                elif status == "FAILURE":
                    fail_reason = result.get("fail_reason", "Unknown error")
                    yield self.create_json_message({
                        "task_id": task_id,
                        "status": "failed",
                        "error": fail_reason
                    })
                    break

                time.sleep(poll_interval)

        except TimeoutError as e:
            yield self.create_json_message({
                "task_id": task_id if task_id else "",
                "status": "timeout",
                "error": str(e)
            })
        except Exception as e:
            yield self.create_json_message({
                "status": "failed",
                "error": str(e)
            })

    def _create_video_task(self, base_url: str, headers: dict, params: dict) -> str:
        """创建视频任务，返回 task_id"""
        response = requests.post(
            f"{base_url}/v2/videos/generations",
            headers=headers,
            json=params,
            timeout=30
        )
        response.raise_for_status()
        return response.json()["task_id"]

    def _query_task(self, base_url: str, headers: dict, task_id: str) -> Dict[str, Any]:
        """查询任务状态"""
        response = requests.get(
            f"{base_url}/v2/videos/generations/{task_id}",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        # 解析响应，提取 video_url
        result = {
            "status": data.get("status"),
            "progress": data.get("progress", ""),
            "fail_reason": data.get("fail_reason", "")
        }

        # 从 data.output 中提取视频 URL
        if data.get("data") and isinstance(data["data"], dict):
            result["video_url"] = data["data"].get("output", "")

        return result
