#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
App Reverse Spec v2.0 - 1:1 落地复刻工作流脚手架调度器
用于一键探测目标类型（Web URL / 客户端安装包 / 源码仓库），初始化标准化 1:1 复刻工作区，
创建原画截图、原版静态资产抽取、OpenAPI 契约、SQL DDL 与 Mock Server 目录结构。
"""

import os
import sys
import json
import argparse
import shutil
from pathlib import Path

# 确保在 Windows 终端下 UTF-8 正常输出
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def sanitize_name(name: str) -> str:
    for ch in [":", "/", "\\", "?", "*", "<", ">", "|", "http", "https"]:
        name = name.replace(ch, "_")
    return name.strip("_")[:50]

def detect_target_type(target: str) -> str:
    if target.startswith("http://") or target.startswith("https://"):
        if "github.com" in target and ("/blob/" not in target and "/issues" not in target):
            return "git_repo"
        return "web_url"
    
    path = Path(target)
    if path.exists():
        if path.is_dir():
            # 探测是否为 Electron 软件目录
            if (path / "resources" / "app.asar").exists() or (path / "resources" / "app").exists():
                return "electron_app_dir"
            return "local_source_dir"
        suffix = path.suffix.lower()
        if suffix in [".exe", ".msi", ".dll"]:
            return "pe_binary"
        elif suffix in [".apk", ".aab"]:
            return "android_pkg"
        elif suffix in [".asar"]:
            return "electron_asar"
        elif suffix in [".zip", ".tar", ".gz"]:
            return "archive_package"
        return "local_file"
    
    return "unknown"

def init_workspace(target: str, target_type: str, base_dir: Path) -> Path:
    safe_name = sanitize_name(target)
    workspace = base_dir / ".analysis" / safe_name
    workspace.mkdir(parents=True, exist_ok=True)
    
    # 建立标准化 1:1 落地复刻所需的资产与协议目录
    (workspace / "assets" / "screenshots").mkdir(parents=True, exist_ok=True)
    (workspace / "assets" / "icons").mkdir(parents=True, exist_ok=True)
    (workspace / "assets" / "fonts").mkdir(parents=True, exist_ok=True)
    (workspace / "contracts").mkdir(parents=True, exist_ok=True)
    (workspace / "schemas").mkdir(parents=True, exist_ok=True)
    (workspace / "traffic").mkdir(parents=True, exist_ok=True)
    (workspace / "extracted").mkdir(parents=True, exist_ok=True)
    (workspace / "mock").mkdir(parents=True, exist_ok=True)
    
    manifest = {
        "version": "2.0.0",
        "target": target,
        "type": target_type,
        "workspace": str(workspace.resolve()),
        "status": "scaffolded",
        "stages": {
            "screenshots_captured": False,
            "assets_extracted": False,
            "traffic_captured": False,
            "event_matrix_built": False,
            "openapi_generated": False,
            "sql_ddl_generated": False,
            "mock_server_ready": False,
            "spec_blueprint_completed": False
        }
    }
    
    with open(workspace / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    # 生成 mock 服务的简易启动脚本说明
    mock_readme = workspace / "mock" / "README.md"
    if not mock_readme.exists():
        mock_readme.write_text(
            "# 本地极速 Mock 服务\n\n"
            "当 `contracts/openapi.yaml` 生成后，运行以下命令一键拉起前端联调 Mock 接口：\n\n"
            "```bash\n"
            "npm install -g @stoplight/prism-cli\n"
            "prism mock ../contracts/openapi.yaml -p 4010\n"
            "```\n",
            encoding="utf-8"
        )
        
    return workspace

def generate_execution_plan(target: str, target_type: str, workspace: Path) -> dict:
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

def main():
    parser = argparse.ArgumentParser(description="App Reverse Spec v2.0 - 1:1 落地复刻工作流脚手架调度器")
    parser.add_argument("target", help="目标 URL、本地文件路径、软件目录或 Git 仓库地址")
    parser.add_argument("--output-dir", default=".", help="工作空间输出根目录")
    
    args = parser.parse_args()
    target = args.target.strip()
    base_dir = Path(args.output_dir).resolve()
    
    target_type = detect_target_type(target)
    workspace = init_workspace(target, target_type, base_dir)
    plan = generate_execution_plan(target, target_type, workspace)
    
    print("\n" + "="*65)
    print("[*] [App Reverse Spec v2.0] 1:1 落地复刻工作流初始化就绪")
    print(f"[+] 目标名称/路径: {target}")
    print(f"[+] 目标类型分类: {target_type}")
    print(f"[+] 复刻工作空间: {workspace}")
    print(f"[+] 核心工具链:   {', '.join(plan['recommended_tools'])}")
    print("="*65)
    print("\n[*] 工业级 1:1 复刻执行步骤:")
    for step in plan["execution_steps"]:
        print(f"  [{step['step']}] {step['name']}")
        if "cmd" in step:
            print(f"      命令: {step['cmd']}")
        if "action" in step:
            print(f"      动作: {step['action']}")
    print("\n" + "="*65)
    print(f"[+] 资产目录已创建: {workspace}/assets (包含 screenshots/ 与 icons/)")
    print(f"[+] 契约目录已创建: {workspace}/contracts (openapi.yaml / .proto)")
    print(f"[+] 数据模型已创建: {workspace}/schemas (可执行 DDL)")
    print(f"[+] 极速Mock已就绪: {workspace}/mock (Prism 联调支持)")
    print("="*65 + "\n")

if __name__ == "__main__":
    main()
