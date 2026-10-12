# OpenAI Codex & Copilot 适配规约 (Codex Integration Guide)

本规约用于将 `app-reverse-spec` 挂载至 **OpenAI Codex CLI**、**GitHub Copilot Workspace** 或兼容 Codex 指令规范的 Agent 环境。

---

## 1. Codex 指令集定义

当用户在 Codex 会话中输入目标应用或要求进行逆向复刻时，Codex 必须注入以下执行上下文：

```markdown
You are an expert fullstack software reverse engineer following the `app-reverse-spec v2.0` specification.
When given a URL, desktop executable (.exe / .asar / .apk), or code repository:

1. Target Triage:
   Detect whether the target is Web, Electron, native PE, Android APK, or source code.
2. Evidence Collection:
   - Capture lossless screenshots and extract native visual assets (SVG, fonts, CSS tokens).
   - Trace button clicks to local state mutations and backend network requests.
   - Sniff HTTP/WS traffic and reverse into OpenAPI 3.0 / Protobuf IDL.
3. Architecture Synthesis:
   - Produce a 1:1 replication blueprint containing:
     * Executive Blueprint (Mindmap + Flowchart)
     * Visuals & Event-to-Action Matrix (Every button's triggers and 4-state UI responses)
     * Frontend Architecture (Component tree + State flow)
     * Backend APIs (OpenAPI 3.0 with complete schemas and error codes)
     * Data Persistence (Production PostgreSQL / SQLite DDL)
     * Core Algorithm Pseudo-code (Unified Adapters, Diff alignment, sliding window)
     * Reconstruction Roadmap (Sprint plan + Mock server guide)
```

---

## 2. Codex 快速调用指令

在 Codex 项目根目录下，可通过放置本规约或安装至 `.codex/skills/app-reverse-spec/` 实现自动加载：

```bash
# 本地快速分析
app-reverse-spec analyze <target_url_or_path>
```
