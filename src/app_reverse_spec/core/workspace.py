import json
from pathlib import Path

def sanitize_name(name: str) -> str:
    for ch in [":", "/", "\\", "?", "*", "<", ">", "|", "http", "https"]:
        name = name.replace(ch, "_")
    return name.strip("_")[:50]

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
