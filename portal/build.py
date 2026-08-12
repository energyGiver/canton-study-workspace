from __future__ import annotations

import base64
import json
import re
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

MERMAID_FENCE = re.compile(
    r"^```mermaid[ \t]*\n(?P<chart>.*?)^```[ \t]*$",
    re.MULTILINE | re.DOTALL | re.IGNORECASE,
)
MEDIA_REFERENCE = re.compile(
    r"(?:!\[[^\]]*\]\((?P<markdown>[^)]+)\)|"
    r"\bsrc=[\"'](?P<html>[^\"']+)[\"'])"
)
MEDIA_SUFFIXES = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}


RESEARCH_PAGES = {
    "research/index.mdx": ("Research Workspace", "overview"),
    "research/favorites.mdx": ("Favorites", "favorites"),
    "research/claims.mdx": ("Claim Ledger", "claims"),
    "research/questions.mdx": ("Open Questions", "questions"),
    "research/progress.mdx": ("Research Progress", "progress"),
    "research/scope.mdx": ("Excluded Pages", "scope"),
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


def refresh_translations() -> int:
    """Refresh Korean pages in an active preview without rebuilding the site."""
    if not SITE_DIR.is_dir():
        raise RuntimeError("Local preview is not prepared. Run python3 -m portal dev first.")
    count = 0
    for source in TRANSLATIONS_DIR.rglob("*.mdx"):
        relative = source.relative_to(TRANSLATIONS_DIR)
        official_path = SOURCE_SITE / relative
        text = source.read_text(encoding="utf-8")
        korean_charts = [match.group("chart") for match in MERMAID_FENCE.finditer(text)]
        if korean_charts:
            if not official_path.is_file():
                raise RuntimeError(f"Official Mermaid source is missing: {relative}")
            official_charts = [
                match.group("chart")
                for match in MERMAID_FENCE.finditer(
                    official_path.read_text(encoding="utf-8")
                )
            ]
            text, _ = _instrument_mermaid(text, official_charts)
        destination = SITE_DIR / "ko" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.is_file() or destination.read_text(encoding="utf-8") != text:
            temporary = destination.with_suffix(destination.suffix + ".tmp")
            temporary.write_text(text, encoding="utf-8")
            temporary.replace(destination)
        count += 1
    _copy_translation_media()
    _extend_docs_config(count)
    return count


def _mermaid_source_marker(chart: str) -> str:
    encoded = base64.b64encode(chart.encode("utf-8")).decode("ascii")
    return (
        '<div className="research-mermaid-source" '
        f'data-research-mermaid-source="{encoded}" />'
    )


def _instrument_mermaid(
    text: str, official_charts: list[str] | None = None
) -> tuple[str, int]:
    count = 0

    def add_source_marker(match: re.Match[str]) -> str:
        nonlocal count
        chart = (
            official_charts[count]
            if official_charts is not None
            else match.group("chart")
        )
        count += 1
        original_fence = match.group(0)
        mirrored_fence = original_fence.replace(match.group("chart"), chart, 1)
        return f"{_mermaid_source_marker(chart)}\n\n{mirrored_fence}"

    instrumented = MERMAID_FENCE.sub(add_source_marker, text)
    if official_charts is not None and count != len(official_charts):
        raise RuntimeError(
            "Korean Mermaid diagram count does not match the official English page"
        )
    return instrumented, count


def _instrument_mermaid_pages() -> int:
    diagrams = 0
    english_pages = [
        path for path in SITE_DIR.rglob("*.mdx") if SITE_DIR / "ko" not in path.parents
    ]
    korean_pages = list((SITE_DIR / "ko").rglob("*.mdx"))
    for path in english_pages:
        text = path.read_text(encoding="utf-8")
        instrumented, page_diagrams = _instrument_mermaid(text)
        if page_diagrams:
            path.write_text(instrumented, encoding="utf-8")
            diagrams += page_diagrams
    for path in korean_pages:
        text = path.read_text(encoding="utf-8")
        korean_charts = [match.group("chart") for match in MERMAID_FENCE.finditer(text)]
        if not korean_charts:
            continue
        relative = path.relative_to(SITE_DIR / "ko")
        official_path = SOURCE_SITE / relative
        if not official_path.is_file():
            raise RuntimeError(f"Official Mermaid source is missing: {relative}")
        official_charts = [
            match.group("chart")
            for match in MERMAID_FENCE.finditer(
                official_path.read_text(encoding="utf-8")
            )
        ]
        instrumented, page_diagrams = _instrument_mermaid(text, official_charts)
        path.write_text(instrumented, encoding="utf-8")
        diagrams += page_diagrams
    return diagrams


def _relative_media_references(text: str) -> set[Path]:
    references: set[Path] = set()
    for match in MEDIA_REFERENCE.finditer(text):
        raw = (match.group("markdown") or match.group("html")).strip()
        value = raw.split("#", 1)[0].split("?", 1)[0]
        if not value or value.startswith(("/", "#", "data:", "http://", "https://")):
            continue
        path = Path(value)
        if path.suffix.lower() in MEDIA_SUFFIXES:
            references.add(path)
    return references


def _copy_translation_media() -> int:
    copied: set[Path] = set()
    for translation in TRANSLATIONS_DIR.rglob("*.mdx"):
        relative_page = translation.relative_to(TRANSLATIONS_DIR)
        official_page = SOURCE_SITE / relative_page
        for reference in _relative_media_references(
            translation.read_text(encoding="utf-8")
        ):
            source = (official_page.parent / reference).resolve()
            try:
                relative_source = source.relative_to(SOURCE_SITE.resolve())
            except ValueError as error:
                raise RuntimeError(
                    f"Translation media escapes the official site: {relative_page} -> {reference}"
                ) from error
            if not source.is_file():
                raise RuntimeError(
                    f"Translation media is missing from the official site: "
                    f"{relative_page} -> {reference}"
                )
            destination = SITE_DIR / "ko" / relative_source
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            copied.add(relative_source)
    return len(copied)


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


def _translated_navigation_products(
    products: list[dict],
    translated_pages: set[str],
    seen_pages: set[str] | None = None,
) -> list[dict]:
    if seen_pages is None:
        seen_pages = set()
    translated_products: list[dict] = []
    for product in products:
        translated_product = {
            key: value
            for key, value in product.items()
            if key not in {"groups", "pages", "root"}
        }
        groups: list[dict] = []
        for group in product.get("groups", []):
            pages = _translated_navigation_entries(
                group.get("pages", []), translated_pages, seen_pages
            )
            if pages:
                groups.append({**group, "pages": pages})
        pages = _translated_navigation_entries(
            product.get("pages", []), translated_pages, seen_pages
        )
        if not groups and not pages:
            continue
        root = product.get("root")
        if isinstance(root, str) and root in translated_pages:
            translated_product["root"] = f"ko/{root}"
        if groups:
            translated_product["groups"] = groups
        if pages:
            translated_product["pages"] = pages
        translated_products.append(translated_product)
    return translated_products


def _localized_navigation(
    products: list[dict],
    korean_products: list[dict],
    global_navigation: dict | None = None,
) -> dict:
    navigation: dict = {}
    if global_navigation:
        navigation["global"] = global_navigation
    if not korean_products:
        navigation["products"] = products
        return navigation

    navigation["languages"] = [
        {
            "language": "en",
            "default": True,
            "products": products,
        },
        {
            "language": "ko",
            "products": korean_products,
        },
    ]
    return navigation


def _extend_docs_config(translation_count: int) -> None:
    config_path = SITE_DIR / "docs.json"
    config = json.loads((SOURCE_SITE / "docs.json").read_text(encoding="utf-8"))
    original_navigation = config.setdefault("navigation", {})
    products = original_navigation.get("products", [])
    products.append(
        {
            "product": "Research Workspace",
            "icon": "microscope",
            "groups": [
                {
                    "group": "Research",
                    "pages": [
                        "research/index",
                        "research/favorites",
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

    translated_pages = {
        str(path.relative_to(TRANSLATIONS_DIR).with_suffix(""))
        for path in TRANSLATIONS_DIR.rglob("*.mdx")
    }
    seen_pages: set[str] = set()
    korean_products = _translated_navigation_products(
        products, translated_pages, seen_pages
    )
    remaining_pages = sorted(translated_pages - seen_pages)
    if remaining_pages:
        korean_products.append(
            {
                "product": "기타 공식 문서",
                "icon": "language",
                "pages": [f"ko/{page}" for page in remaining_pages],
            }
        )
    config["navigation"] = _localized_navigation(
        products,
        korean_products if translation_count else [],
        original_navigation.get("global"),
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
    _copy_translation_media()
    _write_research_pages()
    _extend_docs_config(translation_count)
    _install_overlay_assets()
    _instrument_mermaid_pages()

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
