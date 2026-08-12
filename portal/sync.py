from __future__ import annotations

import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from .build import GENERATED_ROOT, UPSTREAM, build_site
from .content import ContentRepository


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class SyncReport:
    checked_at: str
    previous_commit: str
    target_commit: str
    updated: bool
    changed_files: list[str]
    stale_summaries: list[str]
    stale_translations: list[str]


def _git(*args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(UPSTREAM), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def sync_upstream(update: bool = False) -> SyncReport:
    if not (UPSTREAM / ".git").exists():
        raise RuntimeError("Initialize upstream/cf-docs before checking for updates")
    if _git("status", "--porcelain"):
        raise RuntimeError("The official cf-docs submodule has local changes")

    previous = _git("rev-parse", "HEAD")
    _git("fetch", "--prune", "origin", "main")
    target = _git("rev-parse", "origin/main")
    changed_files = []
    if previous != target:
        changed_files = _git("diff", "--name-only", previous, target, "--", "docs-main").splitlines()
    if update and previous != target:
        _git("checkout", "--detach", target)

    repository = ContentRepository()
    status_rows = repository.status_rows({})
    report = SyncReport(
        checked_at=datetime.now(timezone.utc).isoformat(),
        previous_commit=previous,
        target_commit=target,
        updated=bool(update and previous != target),
        changed_files=changed_files,
        stale_summaries=[row["path"] for row in status_rows if row["summary_stale"]],
        stale_translations=[row["path"] for row in status_rows if row["translation_stale"]],
    )
    output_dir = GENERATED_ROOT / "sync"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "latest.json").write_text(
        json.dumps(asdict(report), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if update:
        build_site()
    return report
