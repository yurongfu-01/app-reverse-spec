# 流程来源与开源项目致谢 (Attributions & Upstream Projects)

本项目 **App-Reverse-Spec** 致力于将全球优秀的逆向工程、Agent 自主探索、流量分析与代码打包工具链进行系统性工程集成。本项目的全流程流水线凝聚了以下开源先驱项目的智慧与成果，特此致敬并标明来源：

---

## 阶段一：黑盒动态抓包与后端 API 逆向生成

### 1. `mitmproxy2swagger`
- **项目地址**: [https://github.com/alufers/mitmproxy2swagger](https://github.com/alufers/mitmproxy2swagger)
- **原始作者**: alufers
- **开源协议**: MIT License
- **在流程中的职责**: 
  - 核心协议转换引擎。
  - 读取浏览器导出的 `.har` 网络请求归档或 `mitmproxy` 抓包日志，自动反向推导 REST API 端点、URL Path 变量、Query 过滤参数、Request Body 及 Response JSON Schema，生成标准的 OpenAPI 3.0 (Swagger) 规范文档。

### 2. `mitmproxy`
- **项目地址**: [https://github.com/mitmproxy/mitmproxy](https://github.com/mitmproxy/mitmproxy)
- **组织团队**: mitmproxy organization
- **开源协议**: MIT License
- **在流程中的职责**:
  - 底层 SSL/TLS 中间人代理服务。
  - 在客户端软件（Electron / 桌面程序 / 移动 App）或无头浏览器背后透明监听所有 HTTP/HTTPS/WebSocket 通信流量，导出流式日志。

### 3. `DocuRift`
- **项目地址**: [https://github.com/tienanr/docurift](https://github.com/tienanr/docurift)
- **原始作者**: tienanr
- **开源协议**: MIT License
- **在流程中的职责**: 
  - 备选实时流量监听分析工具，提供流式 API 结构发现能力。

---

## 阶段二：UI 界面自主探索与交互路径遍历

### 1. `Browser-Use`
- **项目地址**: [https://github.com/browser-use/browser-use](https://github.com/browser-use/browser-use)
- **组织团队**: Browser Use Team
- **开源协议**: MIT License
- **在流程中的职责**:
  - Web 端多模态自主探索智能体。
  - 基于 Playwright 与视觉/DOM 规划，像真实用户一样自主遍历网站的各级导航、表单、Tab 切换与弹窗交互，全自动录制交互路径并截取界面视图。

### 2. `AppAgent`
- **项目地址**: [https://github.com/TencentQQGYLab/AppAgent](https://github.com/TencentQQGYLab/AppAgent)
- **组织团队**: 腾讯 QQ 影像中心团队 (Tencent QQGYLab)
- **开源协议**: Apache-2.0 License
- **在流程中的职责**:
  - 手机端与原生 GUI 的两阶段自主探索架构（Exploration Phase -> Deployment Phase）。
  - 提供多模态界面识别与“应用操作知识库 (Action Knowledge Base)”自动生成思想。

### 3. `UI-TARS`
- **项目地址**: [https://github.com/bytedance/UI-TARS-desktop](https://github.com/bytedance/UI-TARS-desktop)
- **组织团队**: 字节跳动 (ByteDance)
- **开源协议**: Apache-2.0 License
- **在流程中的职责**:
  - 桌面端多模态原生 GUI 操作智能体。
  - 基于端到端视觉感知完成原生窗口的交互动作规划与状态链路捕捉。

---

## 阶段三：UI 控件反向解析与设计系统提取

### 1. `screenshot-to-code`
- **项目地址**: [https://github.com/abi/screenshot-to-code](https://github.com/abi/screenshot-to-code)
- **原始作者**: abi
- **开源协议**: MIT License
- **在流程中的职责**:
  - 视觉逆向组件提炼。
  - 通过多模态大模型分析巡检捕获的界面截图，提取颜色系统、字体规范、网格布局（Flex/Grid）及原子组件层级（Buttons, Tables, Modals, Forms）。

---

## 阶段四：白盒代码仓库解析与上下文打包

### 1. `Repomix` (原 Repopack)
- **项目地址**: [https://github.com/yamadashy/repopack](https://github.com/yamadashy/repopack)
- **原始作者**: Kazuki Yamada (yamadashy)
- **开源协议**: MIT License
- **在流程中的职责**:
  - 全栈代码库上下文极致压缩与结构化打包。
  - 在拥有源码或前端解包代码时，提取核心路由、控制器与 ORM 数据模型，过滤无用依赖，输出大模型最易解析的单一 XML/Markdown 上下文。

### 2. `RepoAgent`
- **项目地址**: [https://github.com/OpenBMB/RepoAgent](https://github.com/OpenBMB/RepoAgent)
- **组织团队**: OpenBMB / 清华团队 / 复旦团队
- **开源协议**: Apache-2.0 License
- **在流程中的职责**:
  - 仓库级代码 AST 解析与多模块文档自动生成。
  - 深度分析代码调用图（Call Graph）与模块依赖关系。

### 3. `Gitingest`
- **项目地址**: [https://github.com/cyclotruc/gitingest](https://github.com/cyclotruc/gitingest)
- **原始作者**: Romain Courtois (cyclotruc)
- **开源协议**: MIT License
- **在流程中的职责**:
  - 针对远程 GitHub 仓库的秒级摘要提取能力。

---

## 阶段五：客户端二进制分析与证据凭据导出

### 1. `REA (Reverse Engineer Anything)`
- **项目地址**: [https://github.com/morluto/rea](https://github.com/morluto/rea)
- **原始作者**: morluto
- **开源协议**: MIT License
- **在流程中的职责**:
  - 针对 Electron asar、PE 二进制可执行文件、Android APK 的静态结构分析与运行时行为捕获，输出标准证据包（Evidence Bundle）。

---

## 阶段六：全景 PRD 规范与质量自检

### 1. `prd-generator`
- **项目地址**: [https://github.com/scalershare/prd-generator](https://github.com/scalershare/prd-generator)
- **组织团队**: Scalershare
- **开源协议**: MIT License
- **在流程中的职责**:
  - 生产级产品需求文档 (PRD) 结构标准与 111 项需求完整性核对清单。

---

## 架构集成总览矩阵

| 逆向阶段 | 核心任务 | 集成的开源项目 | 协议类型 |
| :--- | :--- | :--- | :--- |
| **0. 探测与路由** | 目标类型检测、工作空间初始化 | 自研 `app_reverse_spec.core` | MIT |
| **1. UI 交互探索** | 自主点击、多模态截屏、交互路径记录 | `Browser-Use`, `AppAgent`, `UI-TARS` | MIT / Apache 2.0 |
| **2. API 协议逆向** | 流量嗅探、请求捕获、OpenAPI 自动生成 | `mitmproxy`, `mitmproxy2swagger` | MIT |
| **3. 视觉规范提取** | 截图反向推导 Tailwind / 组件树 | `screenshot-to-code` | MIT |
| **4. 白盒代码解构** | 仓库压缩打包、AST 调用图、数据模型提取 | `Repomix`, `RepoAgent`, `Gitingest` | MIT / Apache 2.0 |
| **5. 客户端解包** | ASAR/PE/APK 静态分析与行为凭据提取 | `REA` | MIT |
| **6. 文档与PRD总装** | 生成六大章节架构蓝图与 Mermaid 规格 | `prd-generator` 规约 + LLM 总装引擎 | MIT |
