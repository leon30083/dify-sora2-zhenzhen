# Dify Sora2 视频生成插件

Dify 工具插件，调用贞贞平台 Sora2 API 实现视频生成。

## 功能特性

- 文生视频（text-to-video）
- 图生视频（image-to-video）
- 异步任务管理
- 并发视频生成

## 安装

```bash
dify plugin install sora2-video-plugin.difypkg
```

## 配置

1. 获取贞贞平台 API Key
2. 在 Dify 中配置插件凭证

## 使用

在 Dify 工作流中添加 Sora2 工具节点

## API 配置

- Base URL: `https://gpt-best.apifox.cn`
- 创建任务：`POST /v2/videos/generations`
- 查询任务：`GET /v2/videos/generations/{task_id}`
