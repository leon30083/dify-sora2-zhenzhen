# 生成 Dify 工具代码

## 功能
根据 API 文档自动生成工具的核心逻辑代码

## 触发命令

```
gen-tool-code text_to_video
```

## 输入参数
- tool_name: 工具名称（text_to_video / image_to_video）
- api_endpoint: API 端点
- parameters: 工具参数列表

## 执行步骤
1. 读取 API 文档
2. 生成 YAML 配置
3. 生成 Python 代码
4. 添加异步轮询逻辑
5. 添加错误处理

## 输出
- tools/{tool_name}.yaml
- tools/{tool_name}.py
