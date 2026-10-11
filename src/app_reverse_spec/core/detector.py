from pathlib import Path

# 兼容 Python 3.7+ 类型定义
try:
    from typing import Literal
    TargetType = Literal[
        "web_url",
        "git_repo",
        "local_source_dir",
        "electron_app_dir",
        "pe_binary",
        "electron_asar",
        "android_pkg",
        "archive_package",
        "local_file",
        "unknown"
    ]
except ImportError:
    TargetType = str

def detect_target_type(target: str) -> str:
    """探测目标输入类型"""
    target = target.strip()
    if target.startswith("http://") or target.startswith("https://"):
        if "github.com" in target and ("/blob/" not in target and "/issues" not in target):
            return "git_repo"
        return "web_url"
    
    path = Path(target)
    if path.exists():
        if path.is_dir():
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
