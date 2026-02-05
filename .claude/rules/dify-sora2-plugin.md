# Dify Sora2 插件开发规则

## 代码风格
- 使用 Python 3.12+ 特性
- 遵循 PEP 8 规范
- 使用类型注解
- 函数添加 docstring

## API 调用规范

### 请求格式

```python
import requests
import time
from typing import Dict, Any

class Sora2Client:
    def __init__(self, api_key: str):
        self.base_url = "https://gpt-best.apifox.cn"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def create_video(self, params) -> str:
        """创建视频任务，返回 task_id"""
        response = requests.post(
            f"{self.base_url}/v2/videos/generations",
            headers=self.headers,
            json=params
        )
        response.raise_for_status()
        return response.json()["task_id"]

    def query_task(self, task_id: str) -> Dict[str, Any]:
        """查询任务状态"""
        response = requests.get(
            f"{self.base_url}/v2/videos/generations/{task_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def poll_until_complete(
        self,
        task_id: str,
        poll_interval: int = 30,
        timeout: int = 300
    ) -> Dict[str, Any]:
        """轮询直到完成或超时"""
        start_time = time.time()
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"任务超时: {task_id}")

            result = self.query_task(task_id)
            status = result.get("status")

            if status == "completed":
                return result
            elif status == "failed":
                raise Exception(f"任务失败: {result.get('error')}")

            time.sleep(poll_interval)
```

## Dify 工具输出格式

```python
from dify_plugin import Tool

class TextToVideoTool(Tool):
    def _invoke(self, tool_parameters: dict) -> str:
        task_id = self.create_video(tool_parameters)

        yield self.create_json_message({
            "task_id": task_id,
            "status": "pending",
            "message": "视频生成任务已提交"
        })

        result = self.poll_until_complete(task_id)

        yield self.create_json_message({
            "task_id": task_id,
            "status": "completed",
            "video_url": result["video_url"],
            "duration": result.get("duration", "unknown")
        })
```

## 错误处理
- 使用 try-except 捕获所有异常
- 超时使用 TimeoutError
- API 错误使用 requests.HTTPError
- 记录详细日志

## 测试要求
- 每个工具必须有单元测试
- 模拟 API 响应
- 测试超时场景
- 测试失败重试
