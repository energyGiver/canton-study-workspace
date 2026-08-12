PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;
PRAGMA busy_timeout = 5000;

CREATE TABLE IF NOT EXISTS page_progress (
    source_id TEXT PRIMARY KEY,
    status TEXT NOT NULL CHECK (status IN ('unreviewed', 'in_progress', 'complete')),
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_settings (
    key TEXT PRIMARY KEY,
    value_json TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS drafts (
    source_id TEXT NOT NULL,
    kind TEXT NOT NULL,
    content TEXT NOT NULL,
    base_file_sha256 TEXT,
    version INTEGER NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (source_id, kind)
);

CREATE TABLE IF NOT EXISTS bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    anchor TEXT,
    note TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS document_cache (
    source_id TEXT PRIMARY KEY,
    source_sha256 TEXT NOT NULL,
    parsed_json TEXT,
    indexed_at TEXT NOT NULL
);

CREATE VIRTUAL TABLE IF NOT EXISTS search_documents USING fts5(
    source_id UNINDEXED,
    path UNINDEXED,
    language UNINDEXED,
    kind UNINDEXED,
    title,
    content,
    tokenize = 'unicode61'
);
