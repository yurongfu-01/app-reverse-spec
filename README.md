# App-Reverse-Spec (全栈应用 1:1 落地复刻与全景规格书工作流)

<p align="center">
  <b>端到端全栈软件与网站逆向复刻工作流：真机原画截屏、原生SVG资产剥离、控件级按键调用链追踪、OpenAPI/Protobuf契约逆向、生产级DDL推导与工业级复刻白皮书生成</b>
</p>

<p align="center">
  <a href="#-流程来源与开源致敬-attributions"><img src="https://img.shields.io/badge/Open_Source-Integrated-blue.svg" alt="Open Source"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"></a>
  <a href="#-支持的目标类型"><img src="https://img.shields.io/badge/Supports-Web_|_Client_|_Source-orange.svg" alt="Targets"></a>
  <a href="skills/app-reverse-spec"><img src="https://img.shields.io/badge/Version-v2.0.0-blueviolet.svg" alt="Version 2.0"></a>
  <a href="skills/app-reverse-spec"><img src="https://img.shields.io/badge/Antigravity-Agent_Native-purple.svg" alt="Agent Ready"></a>
</p>

---

## 📖 项目简介 (Overview)

在日常开发、竞品调研、架构重构或安全审计中，开发者常常需要深入理解并完整复刻一款现有软件或网站：
- **视觉真实度**：如何摆脱“无图脑补”，直接获取全尺寸真机原画截屏与 100% 原版 SVG 图标/字体资产？
- **按键因果闭环**：用户点击某个按钮时，前端状态如何变化？触发了哪个 API/IPC？成功与失败如何渲染？
- **后端工程契约**：如何直接拿到可编译生成前后端 SDK/Controller 桩代码的标准 OpenAPI 3.0 / Protobuf IDL 契约？
- **数据持久化**：如何直接获得可执行的 PostgreSQL / MySQL 建表 DDL 与客户端本地存储 Schema？
- **极速联调**：如何在后端未完成前，10 秒拉起本地 Mock Server 让前端跑通所有功能？

**App-Reverse-Spec v2.0** 综合集成了全球开源社区在**多模态探索、透明流量拦截、协议推导、代码打包与原生资产抽取**领域的顶尖项目，并封装为统一的 CLI 调度工具与 Agent Skill。无论输入的是**在线网站 URL、客户端安装包（.exe / .asar / .apk）还是开源代码仓库**，均能自动规划并执行工业级复刻流水线，直接生成达到“闭眼可落地复刻”工业级标准的架构规格书与工程资产包。

---

## 🏆 流程来源与开源致敬 (Attributions)

本项目绝非凭空产生，而是站在全球优秀开源项目的肩膀上完成的工程化综合集成。**本项目各阶段流水线的核心技术来源如下**：

| 流水线阶段 | 核心任务 | 集成的上游开源项目 | 作者 / 组织 | 开源协议 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 协议逆向** | 网络抓包自动逆向生成 OpenAPI 3.0 / Swagger | [mitmproxy2swagger](https://github.com/alufers/mitmproxy2swagger) | [@alufers](https://github.com/alufers) | MIT |
| **2. 流量拦截** | 客户端/Web 透明 SSL 中间人抓包与监听 | [mitmproxy](https://github.com/mitmproxy/mitmproxy) | mitmproxy org | MIT |
| **3. UI 自主探索** | 基于视觉与 DOM 的浏览器自主巡检与操作 | [Browser-Use](https://github.com/browser-use/browser-use) | Browser Use Team | MIT |
| **4. 移动端探索** | 移动 GUI 自主两阶段探索与知识图谱构建 | [AppAgent](https://github.com/TencentQQGYLab/AppAgent) | 腾讯 QQGYLab | Apache-2.0 |
| **5. 桌面端感知** | 端到端桌面原生 GUI 视觉感知与动作规划 | [UI-TARS](https://github.com/bytedance/UI-TARS-desktop) | 字节跳动 (ByteDance) | Apache-2.0 |
| **6. 视觉规范提炼** | 截屏反向解析为前端组件树与 Tailwind 规范 | [screenshot-to-code](https://github.com/abi/screenshot-to-code) | [@abi](https://github.com/abi) | MIT |
| **7. 仓库上下文打包**| 全栈代码库上下文极致压缩与结构化打包 | [Repomix](https://github.com/yamadashy/repopack) | [@yamadashy](https://github.com/yamadashy) | MIT |
| **8. 代码依赖分析** | 仓库级 AST 代码全局依赖与文档自动维护 | [RepoAgent](https://github.com/OpenBMB/RepoAgent) | OpenBMB / 清华团队 | Apache-2.0 |
| **9. 混合客户端逆向**| 针对 JS/Electron/PE 的结构解包与行为证据包 | [REA](https://github.com/morluto/rea) | [@morluto](https://github.com/morluto) | MIT |
| **10. 需求规范标准**| 生产级 PRD 架构蓝图规约与质量核对标准 | [prd-generator](https://github.com/scalershare/prd-generator) | Scalershare | MIT |

> 详细的各模块来源说明、许可证与调用方式见 [ATTRIBUTIONS.md](ATTRIBUTIONS.md)。

---

## ⚡ 核心架构流水线 (Architecture Pipeline)

```mermaid
flowchart TD
    Target["用户输入目标<br>(网站URL / 客户端程序 / 源码库)"] --> Stage0["阶段 0: 目标自动分类与工作空间隔离<br>(app_reverse_spec.core)"]
    
    subgraph S1["阶段 1: 动态感知与证据链收集"]
        Stage0 -->|Web应用| A1["Browser-Use 自动遍历交互<br>+ mitmproxy 透明抓包"]
        Stage0 -->|客户端/APP| A2["REA / ASAR / APK 解包<br>+ 系统证书代理劫持通信"]
        Stage0 -->|源码/解包库| A3["Repomix 上下文压缩打包<br>+ AST 提取 Router 与 Models"]
    end

    subgraph S2["阶段 2: 逆向解析与标准化"]
        A1 --> B1["mitmproxy2swagger<br>反向生成 openapi.yaml 契约"]
        A2 --> B1
        A1 --> B2["screenshot-to-code<br>提炼 UI 控件树与视觉规范"]
        A3 --> B3["RepoAgent / AST 解析<br>提炼数据流与实体依赖关系"]
    end

    subgraph S3["阶段 3: 多模态总装与企业级 PRD 输出"]
        B1 --> Synthesizer["LLM Agent 综合提炼与规格总装<br>(PRD_TEMPLATE.md 标准规范)"]
        B2 --> Synthesizer
        B3 --> Synthesizer
    end

    Synthesizer --> Delivery["最终交付：全景方案 Markdown<br>1. 系统架构与业务脑图 (Mermaid)<br>2. 页面路由与操作交互时序图<br>3. 前后端完整 API 接口契约<br>4. 数据库 ER 模型与状态机<br>5. 1:1 落地复刻与重构指南"]
```

---

## 📦 安装与快速开始 (Getting Started)

### 1. 克隆仓库与安装依赖
```bash
git clone https://github.com/your-username/app-reverse-spec.git
cd app-reverse-spec

# 安装 Python 基础依赖
pip install -e .

# 可选：安装核心底层工具链
pip install mitmproxy mitmproxy2swagger playwright
playwright install
npm install -g repomix
```

### 2. 作为 CLI 命令行工具使用

#### 探测并规划 Web 网站：
```bash
app-reverse-spec analyze "https://example.com/app"
```

#### 探测本地客户端或源码目录：
```bash
app-reverse-spec analyze "D:/path/to/my-electron-app.asar"
# 或
app-reverse-spec analyze "./my-source-code-dir"
```

#### 查看开源致敬列表：
```bash
app-reverse-spec attributions
```

---

## 🤖 作为 Antigravity / Claude Agent 技能使用

本项目原生支持作为 **Antigravity / Cursor / Claude Code** 技能运行：

1. 将 `skills/app-reverse-spec` 目录复制到您的全局或工作区技能目录中：
   - 全局路径：`~/.gemini/config/skills/app-reverse-spec/`
   - 项目路径：`.agents/skills/app-reverse-spec/`
2. 在对话中直接告诉 Agent：
   > “请帮我分析目标网站 `https://xxx.com`，使用 app-reverse-spec 技能输出完整全景方案。”
3. Agent 将自动激活该技能，调度工具链并按照六大规范章节生成高保真方案！

---

## 🌟 官方开源实战示范包 (Official Showcase)

本项目在 [`examples/chatbox_blueprint/`](examples/chatbox_blueprint/) 完整呈现了一套针对全球 25K+ Stars 顶尖开源 AI 桌面客户端 **[Chatbox](https://github.com/Bin-Huang/chatbox)** 的 1:1 落地复刻工程包：

- 📋 **全景落地复刻规格书**：[`CHATBOX_REPLICATION_SPEC.md`](examples/chatbox_blueprint/CHATBOX_REPLICATION_SPEC.md)（涵盖 7 大章节与无二义性【按键-动作-响应】全局映射矩阵）
- 🔌 **编译级 OpenAPI 3.0 契约**：[`contracts/chatbox_api.yaml`](examples/chatbox_blueprint/contracts/chatbox_api.yaml)（支持直接生成 SDK/Controller 桩代码）
- 🗄️ **双持久化可执行 DDL**：云端 PostgreSQL [`schemas/ddl.sql`](examples/chatbox_blueprint/schemas/ddl.sql) + 本地单机 SQLite FTS5 全文索引 [`schemas/sqlite_client_schema.sql`](examples/chatbox_blueprint/schemas/sqlite_client_schema.sql)
- ⚡ **本地极速 Mock 联调环境**：[`mock/README.md`](examples/chatbox_blueprint/mock/README.md)（基于 Prism 10 秒拉起本地 Mock 服务）

---

## 📑 交付方案标准（输出内容概览）

输出的方案规范严格遵循 [`skills/app-reverse-spec/references/PRD_TEMPLATE.md`](skills/app-reverse-spec/references/PRD_TEMPLATE.md)，包含七大工业级核心章节：

- **1. 系统业务定位与功能全貌**：核心商业模式、功能矩阵拓扑图、核心业务逻辑流（Mermaid）。
- **2. 视觉系统与 UI/UX 交互闭环**：真实截图索引、Design Tokens 规范、**【按键-动作-响应】全局映射矩阵**、交互时序图。
- **3. 前端工程与组件架构**：技术栈选型、组件树拆解、客户端状态流与缓存策略。
- **4. 后端架构与接口协议**：网络拓扑、**可执行级 OpenAPI 3.0 / Protobuf IDL 契约**、全局错误码与重试机制。
- **5. 数据实体模型与持久化层**：Mermaid ER 拓扑、**生产级可执行建表 DDL (SQL)**、客户端本地存储 Schema。
- **6. 核心算法与硬核模块解密**：核心业务算法伪代码（如多模型适配、滑动窗口截断）、原生算力层接口定义。
- **7. 1:1 落地复刻与实施路线图**：Monorepo 脚手架目录规划、本地 Mock 联调指南、4 阶段 Sprint 排期与验收准则 (DoD)。

---

## 🤝 贡献与开源许可

- 本项目采用 [MIT License](LICENSE) 开源协议。
- 各集成模块的版权与许可归属于各自的上游作者与团队，请参阅 [ATTRIBUTIONS.md](ATTRIBUTIONS.md)。
- 欢迎提交 Issue 与 Pull Request 共同完善逆向工具链生态！
