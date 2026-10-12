import sys
import os
import shutil
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
     App-Reverse-Spec v2.0: 全栈应用与网站 1:1 落地复刻规格书生成器
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

def install_skills(agent: str):
    """一键将技能安装并挂载至指定的智能体平台环境"""
    repo_root = Path(__file__).resolve().parents[2]
    skill_src = repo_root / "skills" / "app-reverse-spec"
    adapters_dir = repo_root / "adapters"
    home_dir = Path.home()

    if not skill_src.exists():
        print(f"[-] 错误: 未找到源技能目录: {skill_src}")
        return

    targets = []
    if agent in ["antigravity", "all"]:
        targets.append(("Antigravity", home_dir / ".gemini" / "config" / "skills" / "app-reverse-spec"))
    if agent in ["hermes", "all"]:
        targets.append(("Hermes / HermesStudio", home_dir / ".hermes" / "skills" / "app-reverse-spec"))
    if agent in ["codex", "all"]:
        targets.append(("OpenAI Codex (Global)", home_dir / ".codex" / "skills" / "app-reverse-spec"))
        targets.append(("OpenAI Codex (Local)", Path(".codex") / "skills" / "app-reverse-spec"))
    if agent in ["claude", "all"]:
        targets.append(("Claude Code", home_dir / ".claude" / "skills" / "app-reverse-spec"))

    print(f"\n[*] 正在执行智能体插件与技能安装 (Agent Target: {agent})...")
    
    def _copy_tree_compat(src: Path, dest: Path):
        dest.mkdir(parents=True, exist_ok=True)
        for root, dirs, files in os.walk(str(src)):
            rel = os.path.relpath(root, str(src))
            cur_dest = dest if rel == "." else dest / rel
            cur_dest.mkdir(parents=True, exist_ok=True)
            for f in files:
                shutil.copy2(os.path.join(root, f), str(cur_dest / f))

    for name, dest in targets:
        try:
            _copy_tree_compat(skill_src, dest)
            print(f"[+] 成功适配并安装到 [{name}]: {dest}")
        except Exception as e:
            print(f"[-] 安装到 [{name}] 失败: {e}")

    # 特殊适配：针对 Hermes-Agent 复制原生 Python 工具
    if agent in ["hermes", "all"]:
        hermes_tool_src = adapters_dir / "hermes" / "hermes_tool.py"
        hermes_tool_dest = home_dir / ".hermes" / "tools" / "app_reverse_spec_tool.py"
        if hermes_tool_src.exists():
            try:
                hermes_tool_dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(hermes_tool_src), str(hermes_tool_dest))
                print(f"[+] 成功挂载 Hermes 原生工具到: {hermes_tool_dest}")
            except Exception as e:
                print(f"[-] 挂载 Hermes 原生工具失败: {e}")

    print("\n[*] 插件适配与安装完成！各 Agent 可直接通过自然语言调度此技能。\n")

def main():
    parser = argparse.ArgumentParser(
        description="App Reverse Spec v2.0 - 全栈软件与网站 1:1 落地复刻规格书生成工作流",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # analyze 命令
    analyze_parser = subparsers.add_parser("analyze", help="探测目标并初始化 1:1 复刻工作区")
    analyze_parser.add_argument("target", help="目标 URL、本地文件或源码路径")
    analyze_parser.add_argument("--output-dir", default=".", help="工作空间根目录，默认当前目录")
    
    # install 命令 (新增多智能体平台适配挂载)
    install_parser = subparsers.add_parser("install", help="将技能一键安装适配到指定的 Agent 环境 (Codex, Hermes, Antigravity 等)")
    install_parser.add_argument(
        "--agent",
        choices=["antigravity", "codex", "hermes", "claude", "all"],
        default="all",
        help="目标智能体平台，支持 antigravity, codex, hermes, claude 或 all (默认: all)"
    )

    # attributions 命令
    subparsers.add_parser("attributions", help="查看所有流程来源与上游开源项目致谢")

    # 兼容直接输入 target 的快捷方式 (如 app-reverse-spec https://example.com)
    if len(sys.argv) > 1 and sys.argv[1] not in ["analyze", "install", "attributions", "-h", "--help"]:
        sys.argv.insert(1, "analyze")

    args = parser.parse_args()
    
    if args.command == "attributions":
        print_banner()
        show_attributions()
        return

    if args.command == "install":
        print_banner()
        install_skills(args.agent)
        return

    if args.command == "analyze":
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
        print("[*] 工业级 1:1 落地复刻规划:")
        for step in plan["execution_steps"]:
            print(f"  [{step['step']}] {step['name']}")
            if "cmd" in step:
                print(f"      执行命令: {step['cmd']}")
            if "action" in step:
                print(f"      执行动作: {step['action']}")
            if "alternative" in step:
                print(f"      备选方式: {step['alternative']}")
        print("-" * 65)
        print(f"[+] 资产目录已创建: {workspace}/assets (包含 screenshots/ 与 icons/)")
        print(f"[+] 契约目录已创建: {workspace}/contracts (openapi.yaml / .proto)")
        print(f"[+] 数据模型已创建: {workspace}/schemas (可执行 DDL)")
        print(f"[+] 极速Mock已就绪: {workspace}/mock (Prism 联调支持)")
        print("[+] 提示: 运行完成后，将抓取的数据交由 Agent 套用 PRD 模板一键生成全栈 1:1 落地规格书。\n")
        return

    parser.print_help()

if __name__ == "__main__":
    main()
