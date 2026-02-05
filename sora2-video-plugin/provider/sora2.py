from dify_plugin import ToolProvider
import requests


class Sora2Provider(ToolProvider):
    def _validate_credentials(self, credentials: dict) -> None:
        """验证 API Key 是否有效"""
        api_key = credentials.get("api_key")
        if not api_key:
            raise ValueError("API Key is required")

        # 测试 API 连接
        try:
            response = requests.get(
                "https://ai.t8star.cn/v2/videos/generations",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10
            )
            if response.status_code == 401:
                raise ValueError("Invalid API Key")
        except requests.RequestException as e:
            raise ValueError(f"API connection failed: {str(e)}")
