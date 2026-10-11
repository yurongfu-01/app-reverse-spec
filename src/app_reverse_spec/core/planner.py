from pathlib import Path
from typing import Dict, Any

def generate_execution_plan(target: str, target_type: str, workspace: Path) -> Dict[str, Any]:
    ws_str = str(workspace).replace("\\", "/")
    plan = {
        "target": target,
        "type": target_type,
        "workspace": ws_str,
        "recommended_tools": [],
        "execution_steps": []
    }
    
    if target_type == "web_url":
        plan["recommended_tools"] = ["Playwright", "mitmproxy2swagger", "CDP Event Listener", "Prism"]
        plan["execution_steps"] = [
            {
                "step": 1,
                "name": "真实原画批量截屏 (Visual Screenshots Capture)",
                "action": f'使用 Playwright 高清无损截取关键界面（主页、弹窗、表单、报错态）至 "{ws_str}/assets/screenshots/"'
            },
            {
                "step": 2,
                "name": "网络通信嗅探与 HAR 导出 (Traffic Sniffing)",
                "cmd": f'在浏览器开发者工具 Network 面板导出 HAR，保存至 "{ws_str}/traffic/traffic.har"'
            },
            {
                "step": 3,
                "name": "按键事件与调用链追踪 (Event-to-Network Tracing)",
                "action": '监听 DOM 点击事件并关联网络请求，建立【按键-动作-响应】全局映射矩阵'
            },
            {
                "step": 4,
                "name": "逆向可生成代码的 OpenAPI 契约 (Contract Reverse)",
                "cmd": f'mitmproxy2swagger -i "{ws_str}/traffic/traffic.har" -o "{ws_str}/contracts/openapi.yaml" -p "/" --generate-summaries'
            },
            {
                "step": 5,
                "name": "生成 1:1 落地复刻规格书与 Mock Server",
                "action": f'编写 SQL DDL 到 "{ws_str}/schemas/ddl.sql"，套用 PRD_TEMPLATE 产出最终落地白皮书'
            }
        ]
    elif target_type in ["electron_app_dir", "electron_asar", "pe_binary"]:
        plan["recommended_tools"] = ["asar", "mitmproxy2swagger", "UIAutomation/pywinauto", "Frida", "Prism"]
        plan["execution_steps"] = [
            {
                "step": 1,
                "name": "客户端解包与原生素材 100% 抽取 (Asset Extraction)",
                "action": f'解包目标程序，将原生 SVG 图标、字体、图片批量复制到 "{ws_str}/assets/icons/" 与 "{ws_str}/assets/fonts/"'
            },
            {
                "step": 2,
                "name": "原画级真机截屏采集 (Visual Ground Truth)",
                "action": f'启动客户端并录制全尺寸原画截屏到 "{ws_str}/assets/screenshots/"'
            },
            {
                "step": 3,
                "name": "挂载事件探针与网络监听 (Event & Traffic Trace)",
                "cmd": f'mitmdump -w "{ws_str}/traffic/traffic.flow" --listen-port 8080 (客户端配置 127.0.0.1:8080)'
            },
            {
                "step": 4,
                "name": "导出工程级 API 契约与 SQL DDL",
                "cmd": f'mitmproxy2swagger -i "{ws_str}/traffic/traffic.flow" -o "{ws_str}/contracts/openapi.yaml" -p "/" --generate-summaries'
            },
            {
                "step": 5,
                "name": "输出 1:1 复刻全景白皮书与 Monorepo 脚手架",
                "action": "包含【按键-动作-响应】矩阵、SQL DDL、算法伪代码及本地 Mock 联调指南"
            }
        ]
    elif target_type in ["local_source_dir", "git_repo"]:
        plan["recommended_tools"] = ["Repomix", "Tree-sitter", "RepoAgent"]
        plan["execution_steps"] = [
            {
                "step": 1,
                "name": "代码库全景上下文打包 (Context Packing)",
                "cmd": f'repomix --style xml --output "{ws_str}/codebase-pack.xml" --include "**/src/**,**/routes/**,**/models/**,**/api/**"'
            },
            {
                "step": 2,
                "name": "AST 提取 DDL 与路由拓扑",
                "action": f'提取 ORM Model 并输出可执行 SQL DDL 至 "{ws_str}/schemas/ddl.sql"'
            },
            {
                "step": 3,
                "name": "生成 1:1 重构实施规格书",
                "action": "梳理状态机、抽取 Design Tokens 并输出 Monorepo 实施路线"
            }
        ]
    else:
        plan["recommended_tools"] = ["General AI Analyzer"]
        plan["execution_steps"] = [
            {"step": 1, "name": "通用信息探测", "action": f"自动化探测并初始化 {target} 的逆向工作区"}
        ]
        
    return plan
