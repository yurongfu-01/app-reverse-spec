# 开源工具链集成与使用指引 (Toolchain Guide)

本技能集成的开源项目在整个全栈逆向流水线中各自承担专门的职责。以下是各工具的具体配置、触发方式与输出对接方法。

---

## 1. 动态流量与接口逆向：`mitmproxy` + `mitmproxy2swagger`

### 作用
自动将黑盒软件或网页发送的真实 HTTP/HTTPS 请求与响应，逆向转换为工业标准的 OpenAPI 3.0 / Swagger 规范文档。

### 安装
```bash
pip install mitmproxy mitmproxy2swagger
```

### 两种抓包与解析方式

#### 方式 A：无代理模式（直接浏览器导出 HAR）
1. 在 Chrome / Edge 开发者工具中，打开 `Network (网络)` 标签页。
2. 在目标网站上进行正常业务操作（注册、登录、查询、提交表单、切换 Tab）。
3. 点击网络面板顶部的 `Export HAR... (导出 HAR)`，保存为 `traffic.har`。
4. 执行第一阶段初始化：
   ```bash
   mitmproxy2swagger -i traffic.har -o openapi.yaml -p "/api"
   ```
5. 打开生成的 `openapi.yaml`，去掉需要提取的路由前面的 `ignore:` 前缀。
6. 执行第二阶段生成完整 Schema：
   ```bash
   mitmproxy2swagger -i traffic.har -o openapi.yaml -p "/api" --generate-summaries
   ```

#### 方式 B：客户端/App 代理模式 (mitmdump)
针对桌面软件 (Electron, C++, Qt, Flutter) 或 Android 模拟器：
1. 启动监听：
   ```bash
   mitmdump -w traffic.flow --listen-port 8080
   ```
2. 目标软件设置 HTTP 代理 `127.0.0.1:8080`，并安装 mitmproxy 根证书 (`mitm.it`)。
3. 交互完毕后，将 flow 转换为 HAR 或直接供分析：
   ```bash
   mitmproxy2swagger -i traffic.flow -o openapi.yaml -p "/"
   ```

---

## 2. UI 界面与交互遍历：`Browser-Use`

### 作用
自主在网页上点击各功能入口、子菜单、填写测试数据并记录页面状态。

### 安装与运行
```bash
pip install browser-use playwright
playwright install
```

### 自动化巡检与状态记录脚本样例
```python
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def main():
    agent = Agent(
        task="打开目标网站，依次点击首页主要功能导航、体验核心交互，并将每个重要页面保存截图到 ./screenshots/",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

---

## 3. 代码库全栈上下文压缩：`Repomix` (原 Repopack)

### 作用
当能够获取到前端解包代码（如 Webpack SourceMap 还原）或后端开源仓库时，快速将整个项目的代码目录、关键模块打包成大模型最易解析的单一结构化文档。

### 安装与运行
```bash
# 全局安装
npm install -g repomix

# 针对目标代码库打包，自动忽略无用依赖
repomix --style xml --output codebase-summary.xml
```

### 配合逆向的过滤配置
```bash
# 仅提取路由、控制器与数据模型（最高效提炼系统架构）
repomix --include "**/routes/**,**/controllers/**,**/models/**,**/api/**,**/components/**"
```

---

## 4. 客户端与二进制静态分析：`REA` (Reverse Engineer Anything)

### 作用
针对已编译的客户端应用（Electron asar、PE 二进制、APK、Android 包）：
- 检查二进制布局与依赖库：`binary_overview`, `list_segments`
- 解压或反混淆 JavaScript 运行时：`analyze_javascript_application`
- 提取应用通信行为证据包：`export_evidence_bundle`

---

## 5. UI 视觉规范与组件提炼：`screenshot-to-code`

### 作用
通过视觉截图，直接反推 UI 控件树、布局网格与 CSS 规范（Tailwind/Flexbox）。

### 使用策略
1. 从 `Browser-Use` 截图中筛选出代表性的核心视图（如：仪表盘、列表编辑页、弹窗、表单）。
2. 输入给 Vision 大模型，Prompt 要求：
   > “请分析此截图的 UI 视觉层级，输出：
   > 1. 主色调、辅助色与字体排印规范；
   > 2. 组件拆解树（原子组件、复合组件、业务区块）；
   > 3. 布局结构（Flex/Grid、间距、断点响应式规划）。”

---

## 6. 工具组合速查表

| 分析维度 | 首选开源工具 | 备选方案 | 关键输出成果物 |
| :--- | :--- | :--- | :--- |
| **API 接口与入参/出参** | `mitmproxy2swagger` | `DocuRift` | `openapi.yaml` (OpenAPI 3.0) |
| **UI 与交互路径** | `Browser-Use` | `AppAgent` / Playwright 脚本 | 页面交互流图、核心界面截图集 |
| **代码/解包架构分析** | `Repomix` | `RepoAgent` / `Gitingest` | 代码调用依赖图、模块职责矩阵 |
| **客户端二进制/包体** | `REA` | `jadx` (安卓) / `asar` (桌面) | 解包文件清单、核心类库调用链路 |
| **系统 PRD 与全景蓝图** | 大模型 Agent 编排 | `prd-generator` | 标准化全景方案 Markdown |
