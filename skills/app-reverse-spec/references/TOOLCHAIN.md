# 开源工具链集成与使用指引 (1:1 Toolchain Guide)

本技能集成的开源项目在整个全栈逆向流水线中各自承担专门的职责。以下是各工具的具体配置、触发方式与输出对接方法。

---

## 1. 动态流量与接口契约逆向：`mitmproxy` + `mitmproxy2swagger`

### 作用
自动将黑盒软件或网页发送的真实 HTTP/HTTPS 请求与响应，逆向转换为工业标准的 OpenAPI 3.0 规范文档。

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
   mitmproxy2swagger -i traffic.flow -o openapi.yaml -p "/" --generate-summaries
   ```

---

## 2. 视觉原画截屏与原生资产抽取：`asar` + `Playwright` + PE 资源提取

### 作用
彻底解决“无图脑补”和“山寨图标替换”的顽疾，直接抽取软件内部的 100% 原版 SVG 图标、字体与全尺寸原画截屏。

### 核心操作命令

#### 提取 Electron 客户端的原生静态素材
```bash
# 1. 解包 app.asar
npx @electron/asar extract resources/app.asar ./extracted_app

# 2. 批量查找并复制 SVG 图标与高清图片
powershell -Command "Get-ChildItem -Path ./extracted_app -Recurse -Include *.svg,*.png,*.webp,*.woff2 | Copy-Item -Destination ./assets/ -Force"
```

#### 自动化高清批量原画截屏 (Playwright 脚本样例)
```python
from playwright.sync_api import sync_playwright

def capture_ui_states(url: str, output_dir: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(url)
        page.wait_for_load_state("networkidle")
        
        # 1. 主工作台截图
        page.screenshot(path=f"{output_dir}/dashboard.png")
        
        # 2. 展开菜单或弹窗截图
        if page.locator("button:has-text('新建')").is_visible():
            page.locator("button:has-text('新建')").click()
            page.wait_for_timeout(500)
            page.screenshot(path=f"{output_dir}/create_modal.png")
            
        browser.close()
```

---

## 3. 交互探针与按键事件追踪：CDP + Windows UIA + Frida

### 作用
解决“不知道每个按键能触发什么响应”的难点，通过挂载事件探针与调用栈分析，将每个控件与前端 State、后端 API 紧密绑定。

### 针对 Web / Electron 的 DOM 事件探针 (DevTools CDP)
在控制台或注入脚本中执行，捕获按键与请求的因果链：
```javascript
// 注入网络监听器，打印触发 API 的调用栈
const origFetch = window.fetch;
window.fetch = async function(...args) {
    console.warn('[Network Trace] API Triggered:', args[0]);
    console.trace('[Network Trace] Initiated by:');
    return origFetch.apply(this, args);
};
```

### 针对 Windows 原生软件 (UI Automation / pywinauto)
```python
from pywinauto import Application

app = Application(backend="uia").connect(path="target_app.exe")
main_win = app.top_window()

# 打印所有按钮控件及其 AutomationId
for btn in main_win.descendants(control_type="Button"):
    print(f"控件: {btn.window_text()} | AutomationId: {btn.automation_id()} | Rect: {btn.rectangle()}")
```

---

## 4. 极速 Mock 与前端先行动手：`Prism` / `MSW`

### 作用
在真实后端尚未完全复刻出来之前，利用生成的 `openapi.yaml` 在 30 秒内拉起本地 Mock 服务器，让前端团队能够立即跑通所有按键、弹窗与数据渲染。

### 使用 Prism 一键拉起 Mock Server
```bash
# 全局安装 Prism
npm install -g @stoplight/prism-cli

# 启动 Mock API 服务器 (监听 4010 端口)
prism mock openapi.yaml -p 4010
```
> 前端将 `API_BASE_URL` 指向 `http://localhost:4010`，即可拥有全套具备假数据的完整接口。

---

## 5. 工具组合速查表

| 分析维度 | 首选开源工具 | 备选方案 | 关键输出成果物 |
| :--- | :--- | :--- | :--- |
| **API 接口与入参/出参** | `mitmproxy2swagger` | `Frida` / `wireshark` | `contracts/openapi.yaml` (OpenAPI 3.0) |
| **真实原画截屏** | `Playwright` | OS 原生截屏工具 | `assets/screenshots/*.png` |
| **原生静态素材抽取** | `asar` extract / PE 资源提取 | 浏览器资源另存 | `assets/icons/*.svg`, 字体包 |
| **按键-动作调用链追踪** | CDP 事件钩子 / UIA | `API Monitor` / Frida | 【按键-动作-响应】全局映射矩阵 |
| **代码/解包架构分析** | `Repomix` | `RepoAgent` / `Tree-sitter` | 模块依赖图、核心算法伪代码 |
| **本地快速 Mock 联调** | `Prism` (OpenAPI Mock) | `MSW` (Mock Service Worker) | 本地 Mock 服务, 前端可独立运行 |
| **系统规格书与复刻蓝图** | 大模型 Agent 编排 | `prd-generator` | 标准化 1:1 落地复刻规格书 Markdown |
