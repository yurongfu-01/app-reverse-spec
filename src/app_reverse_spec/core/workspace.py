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
