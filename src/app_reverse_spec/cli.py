import sys
import argparse
from pathlib import Path
from app_reverse_spec.core.detector import detect_target_type
from app_reverse_spec.core.workspace import init_workspace
from app_reverse_spec.core.planner import generate_execution_plan

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def print_banner():
    banner = """
======================================================================
     App-Reverse-Spec: 全栈应用与网站逆向分析 & 全景PRD生成器
======================================================================
"""
    print(banner)

def show_attributions():
    attr_text = """
[项目来源与开源生态致敬 (Attributions)]
1. mitmproxy2swagger (alufers, MIT): 动态流量到 OpenAPI 3.0 规范反向推导
2. mitmproxy (mitmproxy org, MIT): 客户端/Web 透明 SSL 中间人抓包
3. Browser-Use (browser-use team, MIT): 多模态 Agent 网页自主探索与 UI 遍历
4. AppAgent (Tencent QQGYLab, Apache 2.0): 多模态移动 GUI 自主探索与知识图谱构建
5. UI-TARS (ByteDance, Apache 2.0): 原生桌面 GUI 视觉感知与动作规划
6. Repomix (yamadashy, MIT): 仓库级代码上下文压缩与 XML 结构化打包
7. RepoAgent (OpenBMB, Apache 2.0): 代码库 AST 全局依赖与文档自动维护
8. screenshot-to-code (abi, MIT): 视觉截图反向生成组件代码与规范
9. REA (morluto, MIT): 混合客户端与二进制逆向凭据分析
10. prd-generator (scalershare, MIT): 生产级产品需求说明书 (PRD) 规约标准
"""
    print(attr_text)

def main():
    parser = argparse.ArgumentParser(
        description="App Reverse Spec - 全栈软件与网站逆向分析与全景方案生成工作流",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # analyze 命令
    analyze_parser = subparsers.add_parser("analyze", help="探测目标并初始化逆向工作区")
    analyze_parser.add_argument("target", help="目标 URL、本地文件或源码路径")
    analyze_parser.add_argument("--output-dir", default=".", help="工作空间根目录，默认当前目录")
    
    # attributions 命令
    subparsers.add_parser("attributions", help="查看所有流程来源与上游开源项目致谢")

    args = parser.parse_args()
    
    if args.command == "attributions":
        print_banner()
        show_attributions()
        return

    target = args.target if hasattr(args, "target") and args.target else None
    if not target:
        parser.print_help()
        return

    print_banner()
    base_dir = Path(args.output_dir).resolve()
    target_type = detect_target_type(target)
    workspace = init_workspace(target, target_type, base_dir)
    plan = generate_execution_plan(target, target_type, workspace)
    
    print("[*] 目标自动识别完成")
    print(f"[+] 目标名称/路径: {target}")
    print(f"[+] 目标分类:     {target_type}")
    print(f"[+] 隔离工作空间: {workspace}")
    print(f"[+] 推荐开源工具: {', '.join(plan['recommended_tools'])}")
    print("-" * 65)
    print("[*] 自动化执行规划:")
    for step in plan["execution_steps"]:
        print(f"  [{step['step']}] {step['name']}")
        if "cmd" in step:
            print(f"      执行命令: {step['cmd']}")
        if "action" in step:
            print(f"      执行动作: {step['action']}")
        if "alternative" in step:
            print(f"      备选方式: {step['alternative']}")
    print("-" * 65)
    print("[+] 提示: 运行完成后，将抓取的数据交由 Agent 套用 PRD 模板一键生成全栈架构方案。\n")

if __name__ == "__main__":
    main()
