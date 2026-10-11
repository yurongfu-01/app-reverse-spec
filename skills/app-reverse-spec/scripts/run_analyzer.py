#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
App Reverse Spec - 自动化探测与逆向工作流调度器
用于一键探测目标类型（Web URL / 客户端安装包 / 源码仓库），初始化逆向工作区，
并协调 mitmproxy2swagger、repomix、playwright 等开源工具。
"""

import os
import sys
import json
import argparse
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
    (workspace / "screenshots").mkdir(exist_ok=True)
    (workspace / "traffic").mkdir(exist_ok=True)
    (workspace / "extracted").mkdir(exist_ok=True)
    
    manifest = {
        "target": target,
        "type": target_type,
        "workspace": str(workspace.resolve()),
        "status": "initialized",
        "stages": {
            "traffic_captured": False,
            "openapi_generated": False,
            "ui_screenshots_taken": False,
            "code_packaged": False,
            "spec_generated": False
        }
    }
    
    with open(workspace / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
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

def main():
    parser = argparse.ArgumentParser(description="App Reverse Spec - 自动化逆向工作流调度器")
    parser.add_argument("target", help="目标 URL、本地文件路径或 Git 仓库地址")
    parser.add_argument("--output-dir", default=".", help="工作空间输出根目录")
    
    args = parser.parse_args()
    target = args.target.strip()
    base_dir = Path(args.output_dir).resolve()
    
    target_type = detect_target_type(target)
    workspace = init_workspace(target, target_type, base_dir)
    plan = generate_execution_plan(target, target_type, workspace)
    
    print("\n" + "="*60)
    print("[*] [App Reverse Spec] 目标自动识别完成")
    print(f"[+] 目标名称/路径: {target}")
    print(f"[+] 目标分类:     {target_type}")
    print(f"[+] 工作空间目录: {workspace}")
    print(f"[+] 推荐工具链:   {', '.join(plan['recommended_tools'])}")
    print("="*60)
    print("\n[*] 自动化执行计划:")
    for step in plan["execution_steps"]:
        print(f"  [{step['step']}] {step['name']}")
        if "cmd" in step:
            print(f"      命令: {step['cmd']}")
        if "action" in step:
            print(f"      动作: {step['action']}")
        if "alternative" in step:
            print(f"      备选: {step['alternative']}")
    print("\n" + "="*60)
    print("[+] 提示: 按照计划逐步执行上述命令，产出数据后将由 Agent 自动套用 PRD_TEMPLATE 模板生成全景方案。")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
