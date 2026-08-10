#!/usr/bin/env python3
"""Snapshot the Markdown documents listed in the official Canton llms.txt."""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


INDEX_URL = "https://docs.canton.network/llms.txt"
LINK_RE = re.compile(r"^- \[(?P<title>[^]]+)]\((?P<url>https://docs\.canton\.network/[^)]+\.md)\)$")
HEADING_RE = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+?)\s*$")
USER_AGENT = "canton-documentation-research/1.0"


def fetch(url: str, attempts: int = 4) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError) as error:
            if attempt == attempts:
                raise RuntimeError(f"failed to fetch {url}: {error}") from error
            time.sleep(attempt)
    raise AssertionError("unreachable")


def parse_index(raw_index: bytes) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    seen: set[str] = set()
    for line in raw_index.decode("utf-8").splitlines():
        match = LINK_RE.match(line)
        if not match:
            continue
        url = match.group("url")
        if url in seen:
            continue
        seen.add(url)
        entries.append({"title": match.group("title"), "url": url})
    if not entries:
        raise RuntimeError("official index contained no Markdown links")
    return entries


def local_path_for(url: str) -> Path:
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.lstrip("/")
    if not path or ".." in Path(path).parts:
        raise RuntimeError(f"unsafe document path: {url}")
    return Path("corpus/docs") / path


def headings(markdown: str) -> list[dict[str, object]]:
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


def source_id(url: str) -> str:
    """Return an ID that remains stable when the official index is reordered."""
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:10].upper()
    return f"SRC-{digest}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--retrieved-at", help="ISO-8601 timestamp; defaults to current UTC time")
    args = parser.parse_args()

    root = args.root.resolve()
    retrieved_at = args.retrieved_at or dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    retrieval_date = retrieved_at[:10]
    raw_index = fetch(INDEX_URL)
    entries = parse_index(raw_index)

    corpus_dir = root / "corpus"
    docs_dir = corpus_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (corpus_dir / "llms.txt").write_bytes(raw_index)

    def download(entry: dict[str, str]) -> tuple[dict[str, str], bytes]:
        return entry, fetch(entry["url"])

    downloaded: dict[str, bytes] = {}
    failures: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(download, entry): entry for entry in entries}
        for future in concurrent.futures.as_completed(futures):
            entry = futures[future]
            try:
                _, content = future.result()
                downloaded[entry["url"]] = content
            except Exception as error:  # Keep collecting so all failures are reported together.
                failures.append(f"{entry['url']}: {error}")

    if failures:
        for failure in sorted(failures):
            print(failure, file=sys.stderr)
        return 1

    manifest: list[dict[str, object]] = []
    for index, entry in enumerate(entries, start=1):
        content = downloaded[entry["url"]]
        relative_path = local_path_for(entry["url"])
        destination = root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
        markdown = content.decode("utf-8")
        manifest.append(
            {
                "source_id": source_id(entry["url"]),
                "title": entry["title"],
                "source_url": entry["url"],
                "document_path": urllib.parse.urlparse(entry["url"]).path,
                "local_path": relative_path.as_posix(),
                "section_hierarchy": headings(markdown),
                "retrieval_date": retrieval_date,
                "retrieved_at": retrieved_at,
                "sha256": hashlib.sha256(content).hexdigest(),
                "bytes": len(content),
            }
        )

    manifest_path = corpus_dir / "manifest.jsonl"
    with manifest_path.open("w", encoding="utf-8", newline="\n") as handle:
        for item in manifest:
            handle.write(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n")

    metadata = {
        "index_url": INDEX_URL,
        "retrieved_at": retrieved_at,
        "document_count": len(manifest),
        "manifest": "corpus/manifest.jsonl",
        "content_root": "corpus/docs",
        "integrity": "SHA-256 over each downloaded Markdown response body",
    }
    (corpus_dir / "retrieval-metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"downloaded {len(manifest)} official Markdown documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
