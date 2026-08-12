from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_DOCS = ROOT / "upstream" / "cf-docs" / "docs-main"
LOCAL_TRANSLATION_POLICY = ROOT / "data" / "local" / "translation-exclusions.json"


def _navigation_candidates(value: object) -> list[str]:
    candidates: list[str] = []
    if isinstance(value, str):
        candidates.append(value)
    elif isinstance(value, list):
        for item in value:
            candidates.extend(_navigation_candidates(item))
    elif isinstance(value, dict):
        root = value.get("root")
        if isinstance(root, str):
            candidates.append(root)
        pages = value.get("pages")
        if isinstance(pages, list):
            candidates.extend(_navigation_candidates(pages))
        for key in ("products", "groups"):
            nested = value.get(key)
            if isinstance(nested, list):
                candidates.extend(_navigation_candidates(nested))
    return candidates


def official_navigation_paths(source_root: Path = UPSTREAM_DOCS) -> list[str]:
    """Return canonical, file-backed MDX routes in official navigation order."""
    config = json.loads((source_root / "docs.json").read_text(encoding="utf-8"))
    candidates = _navigation_candidates(config.get("navigation", {}))
    paths: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        path = candidate.strip("/")
        if path.endswith(".mdx"):
            path = path[:-4]
        if path in seen or not (source_root / f"{path}.mdx").is_file():
            continue
        seen.add(path)
        paths.append(path)
    return paths


@dataclass(frozen=True)
class TranslationExclusion:
    path: str
    category: str
    reason: str


class TranslationPolicy:
    def __init__(self, policy_path: Path = LOCAL_TRANSLATION_POLICY) -> None:
        self.policy_path = policy_path
        self.exclusions = self._load()
        self.by_path = {item.path: item for item in self.exclusions}

    def _load(self) -> tuple[TranslationExclusion, ...]:
        if not self.policy_path.is_file():
            return ()
        payload = json.loads(self.policy_path.read_text(encoding="utf-8"))
        exclusions: list[TranslationExclusion] = []
        for category in payload.get("categories", []):
            category_id = str(category.get("id", "uncategorized"))
            reason = str(category.get("reason", "")).strip()
            for path in category.get("paths", []):
                exclusions.append(
                    TranslationExclusion(str(path).strip("/"), category_id, reason)
                )
        return tuple(exclusions)

    def excludes(self, path: str) -> bool:
        return path.strip("/").removesuffix(".mdx") in self.by_path

    def ignored_changed_file(self, changed_file: str) -> bool:
        path = changed_file.strip("/")
        if path.startswith("docs-main/"):
            path = path[len("docs-main/") :]
        return path.endswith(".mdx") and self.excludes(path[:-4])
