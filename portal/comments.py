from __future__ import annotations

import json
import os
import re
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .content import ContentRepository, PageRecord, file_sha256


ROOT = Path(__file__).resolve().parents[1]
COMMENTS_ROOT = ROOT / "research" / "comments"
COMMENT_ID = re.compile(r"^CMT-[0-9]{8}T[0-9]{6}Z-[a-f0-9]{8}$")
SOURCE_ID = re.compile(r"^SRC-[A-F0-9]{10}$")
SHA256 = re.compile(r"^[a-f0-9]{64}$")
MIDDLE_DOT = "\u00b7"
LANGUAGES = {"en", "ko"}
MAX_QUOTE = 4_000
MAX_CONTEXT = 256
MAX_COMMENT = 20_000


class CommentConflictError(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _comment_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"CMT-{timestamp}-{uuid.uuid4().hex[:8]}"


def _utf16_length(value: str) -> int:
    return len(value.encode("utf-16-le")) // 2


def _frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("Comment file is missing frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("Comment file has unclosed frontmatter")
    metadata: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"Invalid comment frontmatter line: {line}")
        key, raw = line.split(":", 1)
        value = raw.strip()
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid comment frontmatter value for {key}") from error
        metadata[key.strip()] = str(parsed)
    return metadata, text[end + 5 :]


def _comment_body(body: str) -> str:
    marker = "## Comment\n"
    if marker not in body:
        raise ValueError("Comment file is missing the Comment section")
    return body.split(marker, 1)[1].strip()


def _render(metadata: dict[str, object], content: str) -> str:
    order = [
        "comment_id",
        "source_id",
        "source_path",
        "source_commit",
        "source_sha256",
        "document_sha256",
        "language",
        "heading",
        "selector_type",
        "selector_exact",
        "selector_prefix",
        "selector_suffix",
        "selector_start",
        "selector_end",
        "created_at",
        "created_by",
        "updated_at",
    ]
    lines = ["---"]
    for key in order:
        value = metadata[key]
        if key in {"selector_start", "selector_end"}:
            lines.append(f"{key}: {int(value)}")
        else:
            lines.append(f"{key}: {json.dumps(str(value), ensure_ascii=False)}")
    lines.extend(["---", "", "## Comment", "", content.strip(), ""])
    return "\n".join(lines)


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


class CommentRepository:
    def __init__(
        self,
        content: ContentRepository,
        root: Path = COMMENTS_ROOT,
    ) -> None:
        self.content = content
        self.root = root

    def _paths(self) -> Iterable[Path]:
        if not self.root.is_dir():
            return ()
        return sorted(self.root.glob("SRC-*/*.md"))

    def _document_sha256(self, page: PageRecord, language: str) -> str | None:
        if language == "ko":
            return file_sha256(self.content.translation_path(page))
        return self.content.source_sha256(page)

    def _path_for(self, source_id: str, comment_id: str) -> Path:
        if not SOURCE_ID.fullmatch(source_id) or not COMMENT_ID.fullmatch(comment_id):
            raise ValueError("Invalid comment identifier")
        path = (self.root / source_id / f"{comment_id}.md").resolve()
        if self.root.resolve() not in path.parents:
            raise ValueError("Comment path escapes the comment root")
        return path

    def _find(self, comment_id: str) -> Path:
        if not COMMENT_ID.fullmatch(comment_id):
            raise ValueError("Invalid comment identifier")
        matches = list(self.root.glob(f"SRC-*/{comment_id}.md")) if self.root.is_dir() else []
        if len(matches) != 1:
            raise KeyError(f"Unknown comment: {comment_id}")
        return matches[0]

    @staticmethod
    def _validate_selector(selector: dict) -> dict[str, object]:
        exact = str(selector.get("exact", ""))
        prefix = str(selector.get("prefix", ""))
        suffix = str(selector.get("suffix", ""))
        heading = str(selector.get("heading", ""))
        try:
            start = int(selector.get("start"))
            end = int(selector.get("end"))
        except (TypeError, ValueError) as error:
            raise ValueError("Comment selector positions must be integers") from error
        if not exact or len(exact) > MAX_QUOTE:
            raise ValueError("Comment selection must contain 1 to 4000 characters")
        if len(prefix) > MAX_CONTEXT or len(suffix) > MAX_CONTEXT:
            raise ValueError("Comment selector context is too long")
        if start < 0 or end <= start or end - start != _utf16_length(exact):
            raise ValueError("Comment selector positions do not match the exact quote")
        if not heading or len(heading) > 500:
            raise ValueError("Comment selector heading is required")
        return {
            "type": "TextQuoteSelector",
            "exact": exact,
            "prefix": prefix,
            "suffix": suffix,
            "start": start,
            "end": end,
            "heading": heading,
        }

    @staticmethod
    def _validate_content(content: object) -> str:
        value = str(content).strip()
        if not value or len(value) > MAX_COMMENT:
            raise ValueError("Comment must contain 1 to 20000 characters")
        if MIDDLE_DOT in value:
            raise ValueError("Comment contains forbidden U+00B7")
        return value

    def _read(self, path: Path) -> dict:
        metadata, body = _frontmatter(path.read_text(encoding="utf-8"))
        comment_id = metadata.get("comment_id", "")
        source_id = metadata.get("source_id", "")
        page = self.content.page(source_id)
        language = metadata.get("language", "")
        if path.resolve() != self._path_for(source_id, comment_id):
            raise ValueError(f"Comment path does not match its identifiers: {path}")
        if metadata.get("source_path") != page.path:
            raise ValueError(f"Comment source path does not match the manifest: {path}")
        if language not in LANGUAGES:
            raise ValueError(f"Comment language is invalid: {path}")
        if metadata.get("selector_type") != "TextQuoteSelector":
            raise ValueError(f"Comment selector type is invalid: {path}")
        selector = self._validate_selector(
            {
                "exact": metadata.get("selector_exact", ""),
                "prefix": metadata.get("selector_prefix", ""),
                "suffix": metadata.get("selector_suffix", ""),
                "start": metadata.get("selector_start"),
                "end": metadata.get("selector_end"),
                "heading": metadata.get("heading", ""),
            }
        )
        content = self._validate_content(_comment_body(body))
        source_sha256 = metadata.get("source_sha256", "")
        document_sha256 = metadata.get("document_sha256", "")
        if not SHA256.fullmatch(source_sha256) or not SHA256.fullmatch(document_sha256):
            raise ValueError(f"Comment source hashes are invalid: {path}")
        current_document_sha256 = self._document_sha256(page, language)
        translation = self.content.translation(page)
        return {
            "comment_id": comment_id,
            "source_id": source_id,
            "source_path": page.path,
            "title": page.title,
            "translated_title": translation["metadata"].get("title"),
            "source_commit": metadata.get("source_commit", ""),
            "source_sha256": source_sha256,
            "document_sha256": document_sha256,
            "current_document_sha256": current_document_sha256,
            "stale": (
                current_document_sha256 != document_sha256
                or self.content.source_sha256(page) != source_sha256
            ),
            "language": language,
            "translation_available": translation["available"],
            "heading": selector["heading"],
            "selector": selector,
            "content": content,
            "created_at": metadata.get("created_at", ""),
            "created_by": metadata.get("created_by", "workspace-user"),
            "updated_at": metadata.get("updated_at", ""),
            "file_sha256": file_sha256(path),
        }

    def list(self, page: PageRecord | None = None) -> list[dict]:
        items = [self._read(path) for path in self._paths()]
        if page is not None:
            items = [item for item in items if item["source_id"] == page.source_id]
        return sorted(items, key=lambda item: (item["title"].casefold(), item["created_at"]))

    def create(self, page: PageRecord, payload: dict) -> dict:
        language = str(payload.get("language", ""))
        if language not in LANGUAGES:
            raise ValueError("Comment language must be en or ko")
        current_document_sha256 = self._document_sha256(page, language)
        if current_document_sha256 is None:
            raise ValueError(f"The {language} document is unavailable")
        if payload.get("document_sha256") != current_document_sha256:
            raise CommentConflictError("The document changed before the comment was published")
        selector = self._validate_selector(payload.get("selector") or {})
        content = self._validate_content(payload.get("content", ""))
        comment_id = _comment_id()
        now = _now()
        metadata = {
            "comment_id": comment_id,
            "source_id": page.source_id,
            "source_path": page.path,
            "source_commit": self.content.upstream_commit,
            "source_sha256": self.content.source_sha256(page) or "",
            "document_sha256": current_document_sha256,
            "language": language,
            "heading": selector["heading"],
            "selector_type": selector["type"],
            "selector_exact": selector["exact"],
            "selector_prefix": selector["prefix"],
            "selector_suffix": selector["suffix"],
            "selector_start": selector["start"],
            "selector_end": selector["end"],
            "created_at": now,
            "created_by": str(payload.get("created_by", "workspace-user"))[:200],
            "updated_at": now,
        }
        path = self._path_for(page.source_id, comment_id)
        _atomic_write(path, _render(metadata, content))
        return self._read(path)

    def update(
        self,
        comment_id: str,
        content: object | None,
        base_file_sha256: str | None,
    ) -> dict:
        path = self._find(comment_id)
        current_sha256 = file_sha256(path)
        if base_file_sha256 is not None and current_sha256 != base_file_sha256:
            raise CommentConflictError("The shared comment changed before update")
        metadata, _ = _frontmatter(path.read_text(encoding="utf-8"))
        if content is None:
            raise ValueError("Comment update must include content")
        value = self._validate_content(content)
        metadata["updated_at"] = _now()
        selector_start = int(metadata["selector_start"])
        selector_end = int(metadata["selector_end"])
        rendered: dict[str, object] = {**metadata}
        rendered["selector_start"] = selector_start
        rendered["selector_end"] = selector_end
        _atomic_write(path, _render(rendered, value))
        return self._read(path)

    def delete(self, comment_id: str, base_file_sha256: str | None) -> None:
        path = self._find(comment_id)
        current_sha256 = file_sha256(path)
        if base_file_sha256 is not None and current_sha256 != base_file_sha256:
            raise CommentConflictError("The shared comment changed before deletion")
        path.unlink()
        try:
            path.parent.rmdir()
        except OSError:
            pass

    def validation_errors(self) -> list[str]:
        errors: list[str] = []
        for path in self._paths():
            try:
                self._read(path)
            except (KeyError, ValueError) as error:
                try:
                    label = path.relative_to(ROOT)
                except ValueError:
                    label = path
                errors.append(f"{label}: {error}")
        return errors

    def search_documents(self) -> Iterable[dict[str, str]]:
        for item in self.list():
            prefix = "/ko" if item["language"] == "ko" else ""
            yield {
                "source_id": item["source_id"],
                "path": f"{prefix}/{item['source_path']}?comment={item['comment_id']}",
                "language": item["language"],
                "kind": "comment",
                "title": f"Comment: {item['title']}",
                "content": f"{item['selector']['exact']}\n{item['content']}",
            }
