from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import subprocess
from pathlib import Path

from .content import ROOT, parse_frontmatter
from .inventory import UPSTREAM_DOCS, official_navigation_paths


MANIFEST_PATH = ROOT / "corpus" / "manifest.jsonl"
RETRIEVAL_METADATA_PATH = ROOT / "corpus" / "retrieval-metadata.json"
OFFICIAL_BASE_URL = "https://docs.canton.network"
HEADING_RE = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+?)\s*$")


def _upstream_commit() -> str:
    completed = subprocess.run(
        ["git", "-C", str(UPSTREAM_DOCS.parent), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _source_id(url: str) -> str:
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:10].upper()
    return f"SRC-{digest}"


def _headings(markdown: str) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    in_fence = False
    for line_number, line in enumerate(markdown.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if match:
            result.append(
                {
                    "level": len(match.group("marks")),
                    "title": match.group("title").strip(),
                    "line": line_number,
                }
            )
    return result


def refresh_official_manifest(retrieved_at: str | None = None) -> int:
    """Index every current file-backed official navigation page from cf-docs."""
    timestamp = retrieved_at or dt.datetime.now(dt.timezone.utc).replace(
        microsecond=0
    ).isoformat()
    commit = _upstream_commit()
    records: list[dict[str, object]] = []
    for path in official_navigation_paths():
        source_path = UPSTREAM_DOCS / f"{path}.mdx"
        content = source_path.read_bytes()
        text = content.decode("utf-8")
        frontmatter, body = parse_frontmatter(text)
        source_url = f"{OFFICIAL_BASE_URL}/{path}.md"
        title = str(frontmatter.get("title") or path.rsplit("/", 1)[-1])
        records.append(
            {
                "source_id": _source_id(source_url),
                "title": title,
                "source_url": source_url,
                "document_path": f"/{path}.md",
                "local_path": f"upstream/cf-docs/docs-main/{path}.mdx",
                "section_hierarchy": _headings(body),
                "retrieval_date": timestamp[:10],
                "retrieved_at": timestamp,
                "sha256": hashlib.sha256(content).hexdigest(),
                "bytes": len(content),
                "source_commit": commit,
                "source_format": "mdx",
            }
        )

    MANIFEST_PATH.write_text(
        "".join(
            json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n"
            for item in records
        ),
        encoding="utf-8",
    )
    metadata = {
        "index_source": "upstream/cf-docs/docs-main/docs.json",
        "official_base_url": OFFICIAL_BASE_URL,
        "retrieved_at": timestamp,
        "document_count": len(records),
        "manifest": "corpus/manifest.jsonl",
        "content_root": "upstream/cf-docs/docs-main",
        "source_commit": commit,
        "integrity": "SHA-256 over each official cf-docs MDX source file",
        "scope": "File-backed MDX routes present in official docs.json navigation",
    }
    RETRIEVAL_METADATA_PATH.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return len(records)
