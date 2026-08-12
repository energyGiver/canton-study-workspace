from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "upstream" / "cf-docs"
SOURCE_SITE = UPSTREAM / "docs-main"
GENERATED_ROOT = ROOT / ".generated"
SITE_DIR = GENERATED_ROOT / "site"
TRANSLATIONS_DIR = ROOT / "translations" / "ko"
STATIC_DIR = ROOT / "portal" / "static"


RESEARCH_PAGES = {
    "research/index.mdx": ("Research Workspace", "overview"),
    "research/claims.mdx": ("Claim Ledger", "claims"),
    "research/questions.mdx": ("Open Questions", "questions"),
    "research/progress.mdx": ("Research Progress", "progress"),
    "research/scope.mdx": ("Research Scope", "scope"),
    "research/changes.mdx": ("Upstream Changes", "changes"),
}


@dataclass(frozen=True)
class BuildResult:
    site_dir: Path
    upstream_commit: str
    translation_count: int


def _upstream_commit() -> str:
    completed = subprocess.run(
        ["git", "-C", str(UPSTREAM), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _clear_generated_site() -> None:
    expected_parent = (ROOT / ".generated").resolve()
    resolved = SITE_DIR.resolve()
    if resolved.parent != expected_parent or resolved.name != "site":
        raise RuntimeError(f"Refusing to clear unexpected path: {resolved}")
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)


def _write_research_pages() -> None:
    for relative_path, (title, view) in RESEARCH_PAGES.items():
        destination = SITE_DIR / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            "\n".join(
                [
                    "---",
                    f'title: "{title}"',
                    'description: "Local team research view backed by the Canton documentation corpus"',
                    "---",
                    "",
                    "<Info>This is a local research overlay. Official Canton content remains unchanged.</Info>",
                    "",
                    f'<div id="research-workspace-view" data-research-view="{view}"></div>',
                    "",
                ]
            ),
            encoding="utf-8",
        )


def _copy_translations() -> int:
    if not TRANSLATIONS_DIR.exists():
        return 0
    count = 0
    for source in TRANSLATIONS_DIR.rglob("*.mdx"):
        relative = source.relative_to(TRANSLATIONS_DIR)
        destination = SITE_DIR / "ko" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        count += 1
    return count


def _translated_navigation_entries(
    entries: list, translated_pages: set[str], seen_pages: set[str] | None = None
) -> list:
    if seen_pages is None:
        seen_pages = set()
    translated: list = []
    for entry in entries:
        if isinstance(entry, str):
            if entry in translated_pages and entry not in seen_pages:
                seen_pages.add(entry)
                translated.append(f"ko/{entry}")
            continue
        if not isinstance(entry, dict):
            continue
        nested_pages = _translated_navigation_entries(
            entry.get("pages", []), translated_pages, seen_pages
        )
        if nested_pages:
            translated.append({**entry, "pages": nested_pages})
    return translated


def _extend_docs_config(translation_count: int) -> None:
    config_path = SITE_DIR / "docs.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    products = config.setdefault("navigation", {}).setdefault("products", [])
    products.append(
        {
            "product": "Research Workspace",
            "icon": "microscope",
            "groups": [
                {
                    "group": "Research",
                    "pages": [
                        "research/index",
                        "research/progress",
                        "research/scope",
                        "research/changes",
                    ],
                },
                {
                    "group": "Evidence",
                    "pages": ["research/claims", "research/questions"],
                },
            ],
        }
    )

    languages = [{"language": "en", "default": True, "href": "/"}]
    if translation_count:
        languages.append(
            {
                "language": "ko",
                "href": "/ko/overview/understand/what-is-canton",
            }
        )
    config["navigation"].setdefault("global", {})["languages"] = languages

    translated_pages = {
        str(path.relative_to(TRANSLATIONS_DIR).with_suffix(""))
        for path in TRANSLATIONS_DIR.rglob("*.mdx")
    }
    korean_groups: list[dict] = []
    seen_pages: set[str] = set()
    for product in products:
        for group in product.get("groups", []):
            pages = _translated_navigation_entries(
                group.get("pages", []), translated_pages, seen_pages
            )
            if pages:
                korean_groups.append({"group": group["group"], "pages": pages})
    remaining_pages = sorted(translated_pages - seen_pages)
    if remaining_pages:
        korean_groups.append(
            {
                "group": "기타 공식 문서",
                "pages": [f"ko/{page}" for page in remaining_pages],
            }
        )
    if korean_groups:
        products.append(
            {
                "product": "한글 번역",
                "icon": "language",
                "groups": korean_groups,
            }
        )
    config_path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _install_overlay_assets() -> None:
    javascript = STATIC_DIR / "research-overlay.js"
    stylesheet = STATIC_DIR / "research-overlay.css"
    if javascript.exists():
        shutil.copy2(javascript, SITE_DIR / javascript.name)
    if stylesheet.exists():
        target = SITE_DIR / "styles.css"
        original = target.read_text(encoding="utf-8") if target.exists() else ""
        overlay = stylesheet.read_text(encoding="utf-8")
        target.write_text(
            f"{original.rstrip()}\n\n/* Local Research Workspace */\n{overlay}\n",
            encoding="utf-8",
        )


def build_site() -> BuildResult:
    if not (SOURCE_SITE / "docs.json").is_file():
        raise RuntimeError(
            "Official cf-docs is unavailable. Run git submodule update --init --recursive."
        )

    _clear_generated_site()
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE_SITE, SITE_DIR, symlinks=True)

    translation_count = _copy_translations()
    _write_research_pages()
    _extend_docs_config(translation_count)
    _install_overlay_assets()

    upstream_commit = _upstream_commit()
    metadata = {
        "built_at": datetime.now(timezone.utc).isoformat(),
        "upstream_commit": upstream_commit,
        "source": "upstream/cf-docs/docs-main",
        "translation_count": translation_count,
    }
    (GENERATED_ROOT / "build-metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    return BuildResult(SITE_DIR, upstream_commit, translation_count)
