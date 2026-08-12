from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "corpus" / "manifest.jsonl"
RESEARCH_ROOT = ROOT / "research" / "pages"
TRANSLATION_ROOT = ROOT / "translations" / "ko"
UPSTREAM_DOCS = ROOT / "upstream" / "cf-docs" / "docs-main"
CLAIMS_PATH = ROOT / "claims" / "claim-ledger.md"
QUESTIONS_PATH = ROOT / "questions" / "open-questions.md"


class ContentConflictError(RuntimeError):
    pass


@dataclass(frozen=True)
class PageRecord:
    source_id: str
    title: str
    source_url: str
    path: str
    local_path: str
    published_sha256: str


def file_sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_path(value: str) -> str:
    parsed = urlparse(value)
    path = parsed.path if parsed.scheme or parsed.netloc else value.split("?", 1)[0]
    path = path.split("#", 1)[0].strip().lstrip("/").rstrip("/")
    if path.startswith("ko/"):
        path = path[3:]
    for suffix in (".mdx", ".md", ".html"):
        if path.endswith(suffix):
            path = path[: -len(suffix)]
    return path or "index"


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    metadata: dict[str, object] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, raw = line.split(":", 1)
        value = raw.strip()
        if value in {"null", "~"}:
            parsed: object = None
        elif value in {"true", "false"}:
            parsed = value == "true"
        elif value.startswith(('"', "'")):
            try:
                parsed = json.loads(value) if value.startswith('"') else value[1:-1]
            except json.JSONDecodeError:
                parsed = value.strip('"')
        else:
            parsed = value
        metadata[key.strip()] = parsed
    return metadata, text[end + 5 :]


def render_frontmatter(metadata: dict[str, object]) -> str:
    preferred = [
        "source_id",
        "source_path",
        "source_commit",
        "source_sha256",
        "scope",
        "scope_reason",
        "summary_status",
        "updated_at",
        "updated_by",
    ]
    keys = [key for key in preferred if key in metadata]
    keys.extend(sorted(key for key in metadata if key not in keys))
    lines = ["---"]
    for key in keys:
        value = metadata[key]
        if value is None:
            rendered = "null"
        elif isinstance(value, bool):
            rendered = "true" if value else "false"
        else:
            rendered = json.dumps(str(value), ensure_ascii=False)
        lines.append(f"{key}: {rendered}")
    lines.extend(["---", ""])
    return "\n".join(lines)


def extract_section(body: str, heading: str) -> str:
    pattern = re.compile(
        rf"^## {re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(body)
    return match.group("body").strip() if match else ""


def extract_summary(body: str) -> list[str]:
    section = extract_section(body, "Three-line summary")
    lines = []
    for line in section.splitlines():
        clean = re.sub(r"^\s*(?:[-*]|\d+[.)])\s+", "", line).strip()
        if clean:
            lines.append(clean)
    return lines[:3]


def replace_section(body: str, heading: str, content: str) -> str:
    block = f"## {heading}\n\n{content.strip()}\n"
    pattern = re.compile(
        rf"^## {re.escape(heading)}\s*$\n.*?(?=^##\s|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    if pattern.search(body):
        return pattern.sub(block + "\n", body, count=1).rstrip() + "\n"
    suffix = "\n" if not body or body.endswith("\n") else "\n\n"
    return (body + suffix + block).lstrip()


def parse_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


class ContentRepository:
    def __init__(self) -> None:
        self.pages = self._load_manifest()
        self.by_id = {page.source_id: page for page in self.pages}
        self.by_path = {page.path: page for page in self.pages}
        self.upstream_commit = self._upstream_commit()
        self._source_hashes: dict[str, str | None] = {}

    @staticmethod
    def _upstream_commit() -> str:
        completed = subprocess.run(
            ["git", "-C", str(UPSTREAM_DOCS.parent), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return completed.stdout.strip()

    @staticmethod
    def _load_manifest() -> list[PageRecord]:
        records = []
        for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines():
            item = json.loads(line)
            records.append(
                PageRecord(
                    source_id=item["source_id"],
                    title=item["title"],
                    source_url=item["source_url"],
                    path=canonical_path(item["document_path"]),
                    local_path=item["local_path"],
                    published_sha256=item["sha256"],
                )
            )
        return records

    def page(self, value: str) -> PageRecord:
        page = self.by_id.get(value) or self.by_path.get(canonical_path(value))
        if not page:
            raise KeyError(f"Unknown official document: {value}")
        return page

    @staticmethod
    def _safe_content_path(root: Path, page_path: str, suffix: str) -> Path:
        candidate = (root / f"{page_path}{suffix}").resolve()
        resolved_root = root.resolve()
        if resolved_root not in candidate.parents:
            raise ValueError("Document path escapes the content root")
        return candidate

    def upstream_path(self, page: PageRecord) -> Path:
        return self._safe_content_path(UPSTREAM_DOCS, page.path, ".mdx")

    def research_path(self, page: PageRecord) -> Path:
        return self._safe_content_path(RESEARCH_ROOT, page.path, ".md")

    def translation_path(self, page: PageRecord) -> Path:
        return self._safe_content_path(TRANSLATION_ROOT, page.path, ".mdx")

    def source_sha256(self, page: PageRecord) -> str | None:
        if page.source_id not in self._source_hashes:
            self._source_hashes[page.source_id] = file_sha256(self.upstream_path(page))
        return self._source_hashes[page.source_id]

    def research(self, page: PageRecord) -> dict:
        path = self.research_path(page)
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        metadata, body = parse_frontmatter(text)
        source_sha = self.source_sha256(page)
        saved_source_sha = metadata.get("source_sha256")
        related = extract_section(body, "Related records")
        return {
            "exists": path.is_file(),
            "metadata": metadata,
            "summary": extract_summary(body),
            "notes": extract_section(body, "Research notes"),
            "file_sha256": file_sha256(path),
            "source_sha256": source_sha,
            "stale": bool(path.is_file() and source_sha != saved_source_sha),
            "scope": metadata.get("scope", "included"),
            "scope_reason": metadata.get("scope_reason", ""),
            "summary_status": metadata.get("summary_status", "missing"),
            "related_claim_ids": sorted(set(re.findall(r"CLM-\d{3}", related))),
            "related_question_ids": sorted(set(re.findall(r"OQ-\d{3}", related))),
        }

    def translation(self, page: PageRecord) -> dict:
        path = self.translation_path(page)
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        metadata, _ = parse_frontmatter(text)
        source_sha = self.source_sha256(page)
        saved_source_sha = metadata.get("source_sha256")
        return {
            "available": path.is_file(),
            "path": f"/ko/{page.path}" if path.is_file() else None,
            "metadata": metadata,
            "source_sha256": source_sha,
            "stale": bool(path.is_file() and source_sha != saved_source_sha),
        }

    def details(self, page: PageRecord) -> dict:
        research = self.research(page)
        explicit_claim_ids = set(research["related_claim_ids"])
        claims = [
            item
            for item in self.claims()
            if page.source_id in item["raw"] or item["id"] in explicit_claim_ids
        ]
        question_ids = set(research["related_question_ids"])
        for claim in claims:
            question_ids.update(re.findall(r"OQ-\d{3}", claim["related"]))
        questions = [item for item in self.questions() if item["id"] in question_ids]
        return {
            **asdict(page),
            "research": research,
            "translation": self.translation(page),
            "related_claims": claims,
            "related_questions": questions,
            "upstream_commit": self.upstream_commit,
        }

    def comparison(self, page: PageRecord) -> dict:
        source_path = self.upstream_path(page)
        if not source_path.is_file():
            source_path = ROOT / page.local_path
        if not source_path.is_file():
            raise KeyError(f"Official source is unavailable for {page.source_id}")

        translation_path = self.translation_path(page)
        if not translation_path.is_file():
            raise KeyError(f"Korean translation is unavailable for {page.source_id}")

        _, english_body = parse_frontmatter(
            source_path.read_text(encoding="utf-8", errors="replace")
        )
        _, translated_body = parse_frontmatter(
            translation_path.read_text(encoding="utf-8", errors="replace")
        )
        return {
            "source_id": page.source_id,
            "title": page.title,
            "source_url": page.source_url,
            "source_commit": self.upstream_commit,
            "english": english_body,
            "korean": translated_body,
        }

    def _base_metadata(self, page: PageRecord, existing: dict[str, object]) -> dict:
        return {
            **existing,
            "source_id": page.source_id,
            "source_path": page.path,
            "source_commit": self.upstream_commit,
            "source_sha256": self.source_sha256(page) or "",
            "scope": existing.get("scope", "included"),
            "scope_reason": existing.get("scope_reason", ""),
            "summary_status": existing.get("summary_status", "missing"),
            "updated_at": PortalClock.date(),
            "updated_by": existing.get("updated_by", "workspace-user"),
        }

    @staticmethod
    def _atomic_write(path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                stream.write(text)
            os.replace(temporary_name, path)
        finally:
            if os.path.exists(temporary_name):
                os.unlink(temporary_name)

    def _checked_existing(
        self, page: PageRecord, base_file_sha256: str | None
    ) -> tuple[Path, dict[str, object], str]:
        path = self.research_path(page)
        current_sha = file_sha256(path)
        if base_file_sha256 is not None and current_sha != base_file_sha256:
            raise ContentConflictError("Shared research file changed before publish")
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        metadata, body = parse_frontmatter(text)
        return path, metadata, body

    def publish_summary(
        self,
        page: PageRecord,
        lines: list[str],
        base_file_sha256: str | None,
        status: str,
    ) -> dict:
        cleaned = [line.strip() for line in lines if line.strip()]
        if len(cleaned) != 3:
            raise ValueError("A shared summary must contain exactly three non-empty lines")
        if status not in {"ai_draft", "human_edited", "approved"}:
            raise ValueError("Invalid summary status")
        path, metadata, body = self._checked_existing(page, base_file_sha256)
        metadata = self._base_metadata(page, metadata)
        metadata["summary_status"] = status
        numbered = "\n".join(f"{index}. {line}" for index, line in enumerate(cleaned, 1))
        body = replace_section(body, "Three-line summary", numbered)
        if "## Research notes" not in body:
            body = body.rstrip() + "\n\n## Research notes\n\n"
        self._atomic_write(path, render_frontmatter(metadata) + body.lstrip())
        return self.research(page)

    def publish_scope(
        self,
        page: PageRecord,
        scope: str,
        reason: str,
        base_file_sha256: str | None,
    ) -> dict:
        if scope not in {"included", "excluded"}:
            raise ValueError("Scope must be included or excluded")
        if scope == "excluded" and not reason.strip():
            raise ValueError("An exclusion reason is required")
        path, metadata, body = self._checked_existing(page, base_file_sha256)
        metadata = self._base_metadata(page, metadata)
        metadata["scope"] = scope
        metadata["scope_reason"] = reason.strip()
        if "## Three-line summary" not in body:
            body = replace_section(body, "Three-line summary", "")
        if "## Research notes" not in body:
            body = body.rstrip() + "\n\n## Research notes\n\n"
        self._atomic_write(path, render_frontmatter(metadata) + body.lstrip())
        return self.research(page)

    def claims(self) -> list[dict]:
        items = []
        for line in CLAIMS_PATH.read_text(encoding="utf-8").splitlines():
            if not line.startswith("| CLM-"):
                continue
            cells = parse_table_row(line)
            if len(cells) < 8:
                continue
            source_ids = sorted(set(re.findall(r"SRC-[A-F0-9]{10}", cells[3])))
            sources = [
                {
                    "source_id": source_id,
                    "path": self.by_id[source_id].path,
                    "title": self.by_id[source_id].title,
                }
                for source_id in source_ids
                if source_id in self.by_id
            ]
            items.append(
                {
                    "id": cells[0],
                    "claim": cells[1],
                    "topic": cells[2],
                    "source": cells[3],
                    "evidence": cells[4],
                    "classification": cells[5],
                    "confidence": cells[6],
                    "related": cells[7],
                    "sources": sources,
                    "raw": line,
                }
            )
        return items

    @staticmethod
    def questions() -> list[dict]:
        items = []
        for line in QUESTIONS_PATH.read_text(encoding="utf-8").splitlines():
            if not line.startswith("| OQ-"):
                continue
            cells = parse_table_row(line)
            if len(cells) < 5:
                continue
            items.append(
                {
                    "id": cells[0],
                    "category": cells[1],
                    "question": cells[2],
                    "impact": cells[3],
                    "next_step": cells[4],
                }
            )
        return items

    def status_rows(self, progress: dict[str, str]) -> list[dict]:
        rows = []
        for page in self.pages:
            research = self.research(page)
            translation = self.translation(page)
            rows.append(
                {
                    "source_id": page.source_id,
                    "path": page.path,
                    "title": page.title,
                    "progress": progress.get(page.source_id, "unreviewed"),
                    "scope": research["scope"],
                    "scope_reason": research["scope_reason"],
                    "summary_status": research["summary_status"],
                    "summary_stale": research["stale"],
                    "translation_available": translation["available"],
                    "translation_stale": translation["stale"],
                }
            )
        return rows

    def changes(self) -> list[dict]:
        return [
            row
            for row in self.status_rows({})
            if row["summary_stale"] or row["translation_stale"]
        ]

    def search_documents(self) -> Iterable[dict[str, str]]:
        for page in self.pages:
            published = ROOT / page.local_path
            if published.is_file():
                yield {
                    "source_id": page.source_id,
                    "path": f"/{page.path}",
                    "language": "en",
                    "kind": "official",
                    "title": page.title,
                    "content": published.read_text(encoding="utf-8", errors="replace"),
                }
            translation = self.translation_path(page)
            if translation.is_file():
                yield {
                    "source_id": page.source_id,
                    "path": f"/ko/{page.path}",
                    "language": "ko",
                    "kind": "translation",
                    "title": page.title,
                    "content": translation.read_text(encoding="utf-8", errors="replace"),
                }
            research = self.research_path(page)
            if research.is_file():
                yield {
                    "source_id": page.source_id,
                    "path": f"/{page.path}",
                    "language": "en",
                    "kind": "research",
                    "title": f"Research: {page.title}",
                    "content": research.read_text(encoding="utf-8", errors="replace"),
                }


class PortalClock:
    @staticmethod
    def date() -> str:
        from datetime import date

        return date.today().isoformat()
