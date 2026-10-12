"""
Hermes-Agent & HermesStudio 原生工具适配器 (Hermes Tool Adapter)
适用于 Nous Research hermes-agent 以及 HermesStudio 多智能体集群。
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from app_reverse_spec.core.detector import detect_target_type
    from app_reverse_spec.core.workspace import init_workspace
    from app_reverse_spec.core.planner import generate_execution_plan
except ImportError:
    # 兼容 standalone 路径导入
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
    from app_reverse_spec.core.detector import detect_target_type
    from app_reverse_spec.core.workspace import init_workspace
    from app_reverse_spec.core.planner import generate_execution_plan


class HermesReverseSpecTool:
    """
    Hermes-Agent 工具类：用于启动全栈应用逆向与 1:1 复刻分析流水线。
    """

    name = "app_reverse_spec"
    description = (
        "执行全栈软件或网站逆向分析，自动探测目标类型、初始化 1:1 复刻工程骨架、"
        "规划原画截屏、原版素材抽取、流量嗅探、OpenAPI 契约逆向与 SQL DDL 推导流程。"
    )
    parameters = {
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "目标 URL、本地可执行文件路径 (.exe / .asar / .apk) 或代码仓库路径"
            },
            "output_dir": {
                "type": "string",
                "description": "分析工作空间的保存根目录，默认当前目录",
                "default": "."
            }
        },
        "required": ["target"]
    }

    def run(self, target: str, output_dir: str = ".") -> str:
        """执行逆向规划与脚手架初始化"""
        base_dir = Path(output_dir).resolve()
        target_type = detect_target_type(target)
        workspace = init_workspace(target, target_type, base_dir)
        plan = generate_execution_plan(target, target_type, workspace)
        
        result = {
            "status": "success",
            "target": target,
            "target_type": target_type,
            "workspace_dir": str(workspace),
            "recommended_tools": plan["recommended_tools"],
            "steps": plan["execution_steps"],
            "blueprint_template": "skills/app-reverse-spec/references/PRD_TEMPLATE.md"
        }
        return json.dumps(result, ensure_ascii=False, indent=2)


def get_hermes_tool():
    """供 hermes-agent tools 注册机制动态加载"""
    return HermesReverseSpecTool()
