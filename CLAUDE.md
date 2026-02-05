# Dify Sora2 视频生成插件

## 项目身份
- **名称**：sora2-video-plugin
- **类型**：Dify Tool Plugin
- **作者**：leon luo
- **版本**：v1.0.0

## 核心功能

1. **文生视频**（text_to_video）
   - 输入：prompt, model, duration, aspect_ratio
   - 输出：task_id → video_url

2. **图生视频**（image_to_video）
   - 输入：prompt, image_url, model, duration
   - 输出：task_id → video_url

3. **异步任务管理**
   - 提交任务 → 获取 task_id
   - 轮询状态（30秒间隔）
   - 超时控制（5分钟）

## API 配置

### 贞贞平台
- Base URL: `https://gpt-best.apifox.cn`
- 创建任务：`POST /v2/videos/generations`
- 查询任务：`GET /v2/videos/generations/{task_id}`
- 认证：Bearer Token（API Key）

### 状态码
- `pending`: 等待中
- `processing`: 生成中
- `completed`: 完成（返回 video_url）
- `failed`: 失败

## 技术约束
- 轮询间隔：30秒
- 最大超时：300秒（5分钟）
- 重试次数：最多3次
- 支持模型：sora-2, sora-2-pro

## 禁止事项
- ❌ 硬编码 API Key
- ❌ 无限循环轮询
- ❌ 忽略错误处理
- ❌ 返回原始 API 响应

## 项目结构

```
sora2-video-plugin/
├── provider/
│   ├── sora2.yaml      # 供应商配置
│   └── sora2.py        # 供应商验证逻辑
├── tools/
│   ├── text_to_video.yaml
│   ├── text_to_video.py
│   ├── image_to_video.yaml
│   └── image_to_video.py
├── requirements.txt
└── README.md
```

## 开发检查清单

- [x] 创建项目结构
- [x] 实现 provider 配置和验证
- [x] 实现文生视频工具
- [x] 实现图生视频工具
- [x] 添加异步轮询逻辑
- [x] 添加错误处理
- [ ] 编写测试用例
- [ ] 打包插件
