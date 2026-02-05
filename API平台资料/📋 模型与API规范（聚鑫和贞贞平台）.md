# 📋 模型与API规范（聚鑫和贞贞平台）

上次编辑时间: 2026年2月3日 12:30
优先级: ⭐⭐⭐⭐ 重要
创建时间: 2026年2月3日 11:34
功能标签: 提示词, 规范文档, 视频生成
备注: 动画绘本工具所需的模型与API端点规范，包含文字处理类（Gemini系列）和视频生成类（VEO/Sora2）的完整配置信息
归属中心: 🤖 应用中心
资源状态: ✅ 可用
资源类型: ⚙️ 配置

# 📋 模型与API规范

### 文字处理类

| **模型名称** | **Gemini 端点** | **方法** | **OpenAI 端点** | **方法** |
| --- | --- | --- | --- | --- |
| gemini-3-pro-preview | /v1beta/models/gemini-3-pro-preview:generateContent | POST | /v1/chat/completions | POST |
| gemini-3-pro-preview-thinking | /v1beta/models/gemini-3-pro-preview-thinking:generateContent | POST | /v1/chat/completions | POST |
| gemini-3-flash-preview | /v1beta/models/gemini-3-flash-preview:generateContent | POST | /v1/chat/completions | POST |

### 视频生成类

**核心要求**：

- VEO 和 Sora2 拆分为两个独立的视频生成节点
- 仅使用异步任务方式调用（不使用 chat 格式）
- 优先采用两个平台都支持的【视频统一格式】

#### **聚鑫平台 VEO 模型**

| **模型名称** | **端点** | **方法** | **功能说明** |
| --- | --- | --- | --- |
| veo_3_1-components | /v1/videos | POST | OpenAI 视频格式 |
| veo_3_1-fast-4K | /v1/videos | POST | OpenAI 视频格式，4K 分辨率 |
| veo_3_1-fast-components-4K | /v1/videos | POST | OpenAI 视频格式，4K 分辨率 + 组件 |

**聚鑫平台 Sora2 模型**

| **模型名称** | **端点** | **方法** | **功能说明** |
| --- | --- | --- | --- |
| sora-2-all | /v1/video/create | POST | 视频统一格式（推荐） |
| sora-2-all | /v1/videos | POST | OpenAI 官方视频格式 |
| sora-2-characters | /sora/v1/characters | POST | 创建角色，用于后续 @ 调用 |

贞贞平台视频模型名：

veo3.1-fast、veo3.1-components-4k、veo3.1-components

sora-2

#### 平台文档

### **贞贞平台文档：**

[统一格式接口介绍](https://www.notion.so/2fba3f9269aa808793f6e15f1aad7b9b?pvs=21)

[Veo文生视频](https://www.notion.so/Veo-2fba3f9269aa800ea004d653ec8f3f3e?pvs=21)

[Veo图生视频](https://www.notion.so/Veo-2fba3f9269aa80c4b225f004dbb22402?pvs=21)

[Veo查询任务](https://www.notion.so/Veo-2fba3f9269aa80788514de475782a774?pvs=21)

[Sora2文生视频](https://www.notion.so/Sora2-2fba3f9269aa80c0855ccbe899f395b2?pvs=21)

[Sora2图生视频](https://www.notion.so/Sora2-2fba3f9269aa809582c6d19914f2efd5?pvs=21)

[Sora2故事板视频](https://www.notion.so/Sora2-2fba3f9269aa802a9c0ade3fa6506e21?pvs=21)

[Sora2 使用角色客串](https://www.notion.so/Sora2-2fba3f9269aa80118cd3ea6c4fe89522?pvs=21)

[Sora2查询任务](https://www.notion.so/Sora2-2fba3f9269aa80a3a0d9ecfc060bb508?pvs=21)

### 聚鑫平台文档：

- veo模型-统一视频格式
    
    [状态码](https://www.notion.so/2fba3f9269aa80b989a0defa7e85ee2f?pvs=21)
    
    [创建视频](https://www.notion.so/2fba3f9269aa80469152fd9ab2380253?pvs=21)
    
    [创建视频，带图片](https://www.notion.so/2fba3f9269aa80ccae4bf40b87c08663?pvs=21)
    
    [查询任务](https://www.notion.so/2fba3f9269aa800b94f0d1645f9ca5b9?pvs=21)
    
    [创建视频（参考图）](https://www.notion.so/2fba3f9269aa80fd8e8bfebca6da1e72?pvs=21)
    
- veo模型-opai视频格式
    
    [openai 创建视频，带图片](https://www.notion.so/openai-2fba3f9269aa80c7b2e9cc703edf1f69?pvs=21)
    
    [openai 查询任务](https://www.notion.so/openai-2fba3f9269aa8078b46ed0f995822f3f?pvs=21)
    
    [openai 下载视频](https://www.notion.so/openai-2fba3f9269aa8062a417c11d8809a1ec?pvs=21)
    
- sora2模型-统一视频格式
    
    [创建视频，带图片 sora-2](https://www.notion.so/sora-2-2fba3f9269aa801f8725dfb19a2e2ee0?pvs=21)
    
    [查询任务](https://www.notion.so/2fba3f9269aa8095bff4c9c4433f41a1?pvs=21)
    
    [创建视频 sora-2](https://www.notion.so/sora-2-2fba3f9269aa80cba066eb0deb22b857?pvs=21)
    
    [创建视频 sora-2-pro](https://www.notion.so/sora-2-pro-2fba3f9269aa8065a494ed89fb3dbc4a?pvs=21)
    
    [创建视频 （带 Character）](https://www.notion.so/Character-2fba3f9269aa80baba83fe5f2f1bde3a?pvs=21)
    
- sora2模型-OpenAI视频格式
    
    [openai 创建视频，带图片](https://www.notion.so/openai-2fba3f9269aa80719702dc7892488743?pvs=21)
    
    [使用故事板创建视频](https://www.notion.so/2fba3f9269aa8072b7f3fd15260f09c0?pvs=21)
    
    [openai 创建视频，带图片 私有模式](https://www.notion.so/openai-2fba3f9269aa80dd94eefe081972e17f?pvs=21)
    
    [openai 创建视频（带Character）](https://www.notion.so/openai-Character-2fba3f9269aa80e3866dd4cefb4e1e71?pvs=21)
    
    [openai 编辑视频](https://www.notion.so/openai-2fba3f9269aa80099f7aecf4b6eea547?pvs=21)
    
    [openai 下载视频](https://www.notion.so/openai-2fba3f9269aa804faea1f262b3e35a1c?pvs=21)
    
    [openai 查询任务](https://www.notion.so/openai-2fba3f9269aa808d9ddce9f7281462fd?pvs=21)
    
    [创建角色](https://www.notion.so/2fba3f9269aa80ac8d29cf563f0cbf80?pvs=21)
    

#### 文档参考链接

**聚鑫平台文档**

- [VEO 创建视频（带图片）](https://juxinapi.apifox.cn/api-358938410.md)
- [VEO 创建视频](https://juxinapi.apifox.cn/api-358938411.md)
- [VEO 查询任务](https://juxinapi.apifox.cn/api-358938412.md)
- [Sora2 创建视频（带图片）](https://juxinapi.apifox.cn/api-358938435.md)
- [Sora2 创建视频](https://juxinapi.apifox.cn/api-358938436.md)
- [Sora2 查询任务](https://juxinapi.apifox.cn/api-358938437.md)

**贞贞平台文档**

- [视频生成模型简介](https://gpt-best.apifox.cn/doc-5824160.md)
- [统一格式接口介绍](https://gpt-best.apifox.cn/doc-7324259.md)
- [Veo 文生视频](https://gpt-best.apifox.cn/api-343590061.md)
- [Veo 图生视频](https://gpt-best.apifox.cn/api-343632235.md)
- [Veo 查询任务](https://gpt-best.apifox.cn/api-343593236.md)
- [Sora2 文生视频](https://gpt-best.apifox.cn/api-358024351.md)
- [Sora2 图生视频](https://gpt-best.apifox.cn/api-358024500.md)
- [Sora2 故事板视频](https://gpt-best.apifox.cn/api-385318417.md)
- [Sora2 角色客串](https://gpt-best.apifox.cn/api-369451139.md)
- [Sora2 查询任务](https://gpt-best.apifox.cn/api-358024353.md)