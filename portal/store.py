from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping


VALID_PROGRESS = {"unreviewed", "in_progress", "complete"}
VALID_DRAFT_KINDS = {"summary", "translation", "note"}


class DraftConflictError(RuntimeError):
    pass


class PortalStore:
    def __init__(self, database_path: Path, migrations_dir: Path) -> None:
        self.database_path = database_path
        self.migrations_dir = migrations_dir
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.migrate()

    @staticmethod
    def now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path, timeout=5)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 5000")
        return connection

    def migrate(self) -> None:
        with self.connect() as connection:
            for migration in sorted(self.migrations_dir.glob("*.sql")):
                connection.executescript(migration.read_text(encoding="utf-8"))

    def get_progress(self, source_id: str) -> str:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT status FROM page_progress WHERE source_id = ?", (source_id,)
            ).fetchone()
        return row["status"] if row else "unreviewed"

    def all_progress(self) -> dict[str, str]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT source_id, status FROM page_progress"
            ).fetchall()
        return {row["source_id"]: row["status"] for row in rows}

    def set_progress(self, source_id: str, status: str) -> str:
        if status not in VALID_PROGRESS:
            raise ValueError(f"Invalid progress status: {status}")
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO page_progress(source_id, status, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(source_id) DO UPDATE SET
                    status = excluded.status,
                    updated_at = excluded.updated_at
                """,
                (source_id, status, self.now()),
            )
        return status

    def get_draft(self, source_id: str, kind: str) -> dict | None:
        if kind not in VALID_DRAFT_KINDS:
            raise ValueError(f"Invalid draft kind: {kind}")
        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT source_id, kind, content, base_file_sha256, version, updated_at
                FROM drafts WHERE source_id = ? AND kind = ?
                """,
                (source_id, kind),
            ).fetchone()
        return dict(row) if row else None

    def save_draft(
        self,
        source_id: str,
        kind: str,
        content: str,
        base_file_sha256: str | None,
        expected_version: int | None,
    ) -> dict:
        if kind not in VALID_DRAFT_KINDS:
            raise ValueError(f"Invalid draft kind: {kind}")
        with self.connect() as connection:
            current = connection.execute(
                "SELECT version FROM drafts WHERE source_id = ? AND kind = ?",
                (source_id, kind),
            ).fetchone()
            current_version = current["version"] if current else 0
            if expected_version is not None and expected_version != current_version:
                raise DraftConflictError(
                    f"Draft version changed from {expected_version} to {current_version}"
                )
            next_version = current_version + 1
            updated_at = self.now()
            connection.execute(
                """
                INSERT INTO drafts(
                    source_id, kind, content, base_file_sha256, version, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(source_id, kind) DO UPDATE SET
                    content = excluded.content,
                    base_file_sha256 = excluded.base_file_sha256,
                    version = excluded.version,
                    updated_at = excluded.updated_at
                """,
                (
                    source_id,
                    kind,
                    content,
                    base_file_sha256,
                    next_version,
                    updated_at,
                ),
            )
        return {
            "source_id": source_id,
            "kind": kind,
            "content": content,
            "base_file_sha256": base_file_sha256,
            "version": next_version,
            "updated_at": updated_at,
        }

    def rebuild_search(self, documents: Iterable[Mapping[str, str]]) -> int:
        rows = [
            (
                item["source_id"],
                item["path"],
                item["language"],
                item["kind"],
                item["title"],
                item["content"],
            )
            for item in documents
        ]
        with self.connect() as connection:
            connection.execute("DELETE FROM search_documents")
            connection.executemany(
                """
                INSERT INTO search_documents(
                    source_id, path, language, kind, title, content
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
        return len(rows)

    @staticmethod
    def _fts_query(query: str) -> str:
        tokens = re.findall(r"[^\W_]+", query, flags=re.UNICODE)
        return " AND ".join(f'"{token}"*' for token in tokens[:12])

    def search(self, query: str, limit: int = 30) -> list[dict]:
        match = self._fts_query(query)
        if not match:
            return []
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    source_id,
                    path,
                    language,
                    kind,
                    title,
                    snippet(search_documents, 5, '<mark>', '</mark>', ' ... ', 24)
                        AS snippet,
                    bm25(search_documents) AS rank
                FROM search_documents
                WHERE search_documents MATCH ?
                ORDER BY rank
                LIMIT ?
                """,
                (match, max(1, min(limit, 100))),
            ).fetchall()
        return [dict(row) for row in rows]

    def settings(self) -> dict[str, object]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT key, value_json FROM user_settings"
            ).fetchall()
        return {row["key"]: json.loads(row["value_json"]) for row in rows}

    def set_setting(self, key: str, value: object) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO user_settings(key, value_json, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    value_json = excluded.value_json,
                    updated_at = excluded.updated_at
                """,
                (key, json.dumps(value), self.now()),
            )
