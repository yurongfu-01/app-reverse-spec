# Chatbox 本地极速 Mock Server 联调指南

在无真实 LLM Key 或后端服务就绪前，前端团队可在 10 秒内启动本地 Mock API，独立跑通会话创建、历史加载与消息交互。

---

### 1. 安装 Stoplight Prism
```bash
npm install -g @stoplight/prism-cli
```

### 2. 启动本地 Mock API 服务器
在当前 `chatbox_blueprint` 根目录下执行：
```bash
prism mock contracts/chatbox_api.yaml -p 4010
```

### 3. 前端环境配置
将前端工程的 `.env.development` 环境变量指向 Mock 地址：
```env
VITE_API_BASE_URL=http://localhost:4010
```

### 4. 验证联调
- 获取模型列表：`curl http://localhost:4010/models`
- 发送对话：`curl -X POST http://localhost:4010/chat/completions -H "Content-Type: application/json" -d '{"model":"gpt-4o","messages":[{"role":"user","content":"hello"}]}'`
