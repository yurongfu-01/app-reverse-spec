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
        plan["recommended_tools"] = ["Browser-Use", "mitmproxy2swagger", "Wappalyzer"]
        plan["execution_steps"] = [
            {
                "step": 1,
                "name": "启动网络流量监听 (Network Interception)",
                "cmd": f'mitmdump -w "{ws_str}/traffic/traffic.flow" --listen-port 8080',
                "alternative": f'在浏览器打开 {target}，操作核心功能后从 Network 面板导出 HAR 到 "{ws_str}/traffic/traffic.har"'
            },
            {
                "step": 2,
                "name": "多模态 UI 巡检与截图 (UI Exploration)",
                "action": f'使用 Browser-Use 遍历 {target} 的关键页面与菜单，截图保存至 "{ws_str}/screenshots/"'
            },
            {
                "step": 3,
                "name": "逆向生成 OpenAPI 契约 (API Extraction)",
                "cmd": f'mitmproxy2swagger -i "{ws_str}/traffic/traffic.har" -o "{ws_str}/openapi.yaml" -p "/" --generate-summaries'
            },
            {
                "step": 4,
                "name": "全景文档总装 (Document Synthesis)",
                "action": "加载截图与 openapi.yaml，套用 PRD_TEMPLATE.md 生成最终全栈方案 Markdown"
            }
        ]
    elif target_type in ["pe_binary", "electron_asar", "android_pkg"]:
        plan["recommended_tools"] = ["REA", "mitmproxy", "screenshot-to-code", "jadx"]
        plan["execution_steps"] = [
            {
                "step": 1,
                "name": "静态解包与资源提取 (Static Extraction)",
                "action": f'针对 {target_type} 执行解包提取资源与前端 JS 代码到 "{ws_str}/extracted/"'
            },
            {
                "step": 2,
                "name": "客户端网络通信监听 (API Sniffing)",
                "cmd": f'配置代理 127.0.0.1:8080 并启动软件，截获通信包至 "{ws_str}/traffic/traffic.flow"'
            },
            {
                "step": 3,
                "name": "OpenAPI 生成与界面提取",
                "cmd": f'mitmproxy2swagger -i "{ws_str}/traffic/traffic.flow" -o "{ws_str}/openapi.yaml" -p "/"'
            },
            {
                "step": 4,
                "name": "全景方案与复刻蓝图生成",
                "action": "汇总客户端架构、通信协议、UI控件树生成高保真重构文档"
            }
        ]
    elif target_type in ["local_source_dir", "git_repo"]:
        plan["recommended_tools"] = ["Repomix", "RepoAgent"]
        plan["execution_steps"] = [
            {
                "step": 1,
                "name": "代码库全景上下文打包 (Context Packing)",
                "cmd": f'repomix --style xml --output "{ws_str}/codebase-pack.xml" --include "**/src/**,**/routes/**,**/models/**,**/api/**"'
            },
            {
                "step": 2,
                "name": "AST 依赖与架构解析",
                "action": "解析路由文件与 ORM 模型，自动绘制 Mermaid 架构拓扑与 ER 数据图"
            },
            {
                "step": 3,
                "name": "生成系统白皮书与开发文档",
                "action": "按照 PRD_TEMPLATE 提取业务逻辑、核心算法并生成全景方案"
            }
        ]
    else:
        plan["recommended_tools"] = ["General AI Analyzer"]
        plan["execution_steps"] = [
            {"step": 1, "name": "通用信息探测", "action": f"人工或自动化补充关于 {target} 的背景资料"}
        ]
        
    return plan
