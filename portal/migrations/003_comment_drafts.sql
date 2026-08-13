CREATE TABLE IF NOT EXISTS comment_drafts (
    source_id TEXT NOT NULL,
    language TEXT NOT NULL CHECK (language IN ('en', 'ko')),
    selector_json TEXT NOT NULL,
    content TEXT NOT NULL,
    version INTEGER NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (source_id, language)
);
