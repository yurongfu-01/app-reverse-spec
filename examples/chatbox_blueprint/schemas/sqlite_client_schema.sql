-- Chatbox 桌面客户端本地 SQLite 存储结构 (纯本地单机离线运行)
-- 包含本地偏好设置、本地会话、离线消息历史及 FTS5 全文搜索支持

PRAGMA foreign_keys = ON;

-- 1. 本地全局键值配置表 (Settings & API Keys)
CREATE TABLE IF NOT EXISTS local_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
);

-- 2. 本地会话表
CREATE TABLE IF NOT EXISTS local_sessions (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL DEFAULT '新对话',
    model_provider TEXT NOT NULL DEFAULT 'openai',
    model_name TEXT NOT NULL DEFAULT 'gpt-4o',
    system_prompt TEXT DEFAULT '',
    temperature REAL DEFAULT 0.7,
    max_tokens INTEGER DEFAULT 4096,
    is_pinned INTEGER DEFAULT 0,
    created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    updated_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
);
CREATE INDEX IF NOT EXISTS idx_local_sessions_updated_at ON local_sessions(updated_at DESC);

-- 3. 本地消息历史表
CREATE TABLE IF NOT EXISTS local_messages (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES local_sessions(id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    model_used TEXT,
    tokens_prompt INTEGER DEFAULT 0,
    tokens_completion INTEGER DEFAULT 0,
    created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
);
CREATE INDEX IF NOT EXISTS idx_local_messages_session_id ON local_messages(session_id);

-- 4. SQLite FTS5 全文搜索虚拟表 (毫秒级本地全局检索)
CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
    message_id UNINDEXED,
    session_id UNINDEXED,
    content,
    tokenize = 'unicode61'
);

-- 触发器：自动同步消息到全文检索表
CREATE TRIGGER IF NOT EXISTS trg_messages_ai AFTER INSERT ON local_messages
BEGIN
    INSERT INTO messages_fts(message_id, session_id, content)
    VALUES (new.id, new.session_id, new.content);
END;

CREATE TRIGGER IF NOT EXISTS trg_messages_ad AFTER DELETE ON local_messages
BEGIN
    DELETE FROM messages_fts WHERE message_id = old.id;
END;
