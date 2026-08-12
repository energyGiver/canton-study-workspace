from __future__ import annotations

from dataclasses import dataclass
from collections import Counter
import json
from pathlib import Path
import re

from .content import ContentRepository, TRANSLATION_ROOT, canonical_path


MIDDLE_DOT = "\u00b7"


def _frontmatter_syntax_errors(text: str) -> list[str]:
    if not text.startswith("---\n"):
        return ["missing opening delimiter"]
    end = text.find("\n---\n", 4)
    if end == -1:
        return ["missing closing delimiter"]

    errors: list[str] = []
    for line_number, line in enumerate(text[4:end].splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        raw = line.split(":", 1)[1].strip()
        if raw.startswith('"'):
            try:
                json.loads(raw)
            except json.JSONDecodeError:
                errors.append(f"line {line_number} has an invalid double-quoted value")
    return errors


def _heading_levels(text: str) -> list[int]:
    return [len(match.group(1)) for match in re.finditer(r"^(#{1,6})\s+", text, re.MULTILINE)]


def _imports(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip().startswith("import ")]


def _mdx_components(text: str) -> Counter[str]:
    components = Counter(re.findall(r"</?([A-Z][A-Za-z0-9.]*)\b", text))
    components.pop("Warning", None)
    return components


def _fenced_blocks(text: str) -> list[tuple[str, str]]:
    return [
        (match.group(1).strip(), match.group(2))
        for match in re.finditer(r"^```([^\n]*)\n(.*?)^```\s*$", text, re.MULTILINE | re.DOTALL)
    ]


def _has_unclosed_fence(text: str) -> bool:
    in_fence = False
    for line in text.splitlines():
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
    return in_fence


def _links(text: str) -> list[str]:
    return re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)


def _normalize_code_whitespace(text: str) -> str:
    return re.sub(r"[ \t]+(?=\n|$)", "", text)


def _scope_profile_errors(repository: ContentRepository) -> list[str]:
    profile = repository.scope_profile
    errors: list[str] = []
    required_text = ("profile_id", "title", "decision")
    for key in required_text:
        if not isinstance(profile.get(key), str) or not profile[key].strip():
            errors.append(f"scope profile {key} is required")

    conditions = profile.get("conditions")
    if not isinstance(conditions, list) or not conditions:
        errors.append("scope profile conditions must be a non-empty list")

    matched_by_path: dict[str, list[str]] = {}
    rule_ids: set[str] = set()
    rules = profile.get("rules")
    if not isinstance(rules, list) or not rules:
        return errors + ["scope profile rules must be a non-empty list"]

    for rule in rules:
        rule_id = str(rule.get("id", "")).strip()
        label = str(rule.get("label", "")).strip()
        reason = str(rule.get("reason", "")).strip()
        if not rule_id or not label or not reason:
            errors.append("every scope profile rule requires id, label, and reason")
            continue
        if rule_id in rule_ids:
            errors.append(f"scope profile rule id is duplicated: {rule_id}")
        rule_ids.add(rule_id)

        exact_paths = set(rule.get("paths", []))
        prefixes = set(rule.get("path_prefixes", []))
        unknown = sorted(exact_paths - repository.by_path.keys())
        for path in unknown:
            errors.append(f"scope profile path is not in the manifest: {path}")

        matched = {
            page.path
            for page in repository.pages
            if page.path in exact_paths
            or any(page.path.startswith(prefix) for prefix in prefixes)
        }
        if not matched:
            errors.append(f"scope profile rule matches no pages: {rule_id}")
        for path in matched:
            matched_by_path.setdefault(path, []).append(rule_id)

    for path, matching_rules in sorted(matched_by_path.items()):
        if len(matching_rules) > 1:
            errors.append(
                "scope profile page matches multiple rules: "
                f"{path} ({', '.join(matching_rules)})"
            )

    expected = profile.get("expected_excluded_pages")
    if not isinstance(expected, int):
        errors.append("scope profile expected_excluded_pages must be an integer")
    elif len(matched_by_path) != expected:
        errors.append(
            "scope profile excluded-page count changed: "
            f"expected {expected}, found {len(matched_by_path)}"
        )

    if MIDDLE_DOT in json.dumps(profile, ensure_ascii=False):
        errors.append("scope profile contains forbidden U+00B7")
    return errors


@dataclass(frozen=True)
class ValidationReport:
    pages: int
    summaries: int
    translations: int
    errors: tuple[str, ...]
    warnings: tuple[str, ...]

    @property
    def valid(self) -> bool:
        return not self.errors


def validate_workspace() -> ValidationReport:
    repository = ContentRepository()
    errors: list[str] = _scope_profile_errors(repository)
    warnings: list[str] = []
    summaries = 0
    translations = 0
    known_translation_paths: set[Path] = set()

    for page in repository.pages:
        research = repository.research(page)
        translation = repository.translation(page)

        if research["exists"]:
            summaries += 1
            metadata = research["metadata"]
            if metadata.get("source_id") != page.source_id:
                errors.append(f"{page.path}: research source_id does not match the manifest")
            if metadata.get("source_path") != page.path:
                errors.append(f"{page.path}: research source_path does not match the manifest")
            if not metadata.get("source_commit"):
                errors.append(f"{page.path}: research source_commit is required")
            if not metadata.get("source_sha256"):
                errors.append(f"{page.path}: research source_sha256 is required")
            if len(research["summary"]) not in {0, 3}:
                errors.append(f"{page.path}: summary must contain exactly three lines")
            if research["stale"]:
                warnings.append(f"{page.path}: shared summary requires source review")

        if translation["available"]:
            translations += 1
            translation_path = repository.translation_path(page)
            known_translation_paths.add(translation_path.resolve())
            translation_text = translation_path.read_text(encoding="utf-8")
            for syntax_error in _frontmatter_syntax_errors(translation_text):
                errors.append(f"{page.path}: translation frontmatter {syntax_error}")
            source_path = repository.official_source_path(page)
            source_text = (
                source_path.read_text(encoding="utf-8") if source_path.is_file() else ""
            )
            metadata = translation["metadata"]
            if metadata.get("source_id") != page.source_id:
                errors.append(f"{page.path}: translation source_id does not match the manifest")
            if metadata.get("source_path") != page.path:
                errors.append(f"{page.path}: translation source_path does not match the manifest")
            if not metadata.get("source_commit"):
                errors.append(f"{page.path}: translation source_commit is required")
            if not metadata.get("source_sha256"):
                errors.append(f"{page.path}: translation source_sha256 is required")
            if metadata.get("translation_status") not in {
                "ai_draft",
                "human_edited",
                "approved",
            }:
                errors.append(f"{page.path}: translation_status is invalid")
            if not metadata.get("translated_at"):
                errors.append(f"{page.path}: translation translated_at is required")
            if "reviewed_by" not in metadata:
                errors.append(f"{page.path}: translation reviewed_by is required")
            if not metadata.get("title"):
                errors.append(f"{page.path}: translated title is required")
            if "<Warning>" not in translation_text or "</Warning>" not in translation_text:
                errors.append(f"{page.path}: unofficial translation Warning is required")
            official_url = page.source_url.removesuffix(".md")
            warning_url = (
                page.source_url if page.source_url in translation_text else official_url
            )
            if warning_url not in translation_text:
                errors.append(f"{page.path}: Warning must link to the official English page")
            if _has_unclosed_fence(translation_text):
                errors.append(f"{page.path}: translation has an unclosed code fence")
            if MIDDLE_DOT in translation_text:
                errors.append(f"{page.path}: translation contains forbidden U+00B7")
            if source_text:
                if _heading_levels(source_text) != _heading_levels(translation_text):
                    errors.append(f"{page.path}: translated heading hierarchy changed")
                if _imports(source_text) != _imports(translation_text):
                    errors.append(f"{page.path}: translated MDX imports changed")
                if _mdx_components(source_text) != _mdx_components(translation_text):
                    errors.append(f"{page.path}: translated MDX component structure changed")
                source_links = Counter(_links(source_text))
                translated_links = Counter(_links(translation_text))
                translated_links[warning_url] -= 1
                if translated_links[warning_url] <= 0:
                    translated_links.pop(warning_url, None)
                if source_links != translated_links:
                    errors.append(f"{page.path}: translated Markdown link targets changed")
                for marker in (r"\<", r"\>"):
                    if source_text.count(marker) != translation_text.count(marker):
                        errors.append(
                            f"{page.path}: translated escaped angle marker count changed"
                        )
                source_blocks = _fenced_blocks(source_text)
                translated_blocks = _fenced_blocks(translation_text)
                if [language for language, _ in source_blocks] != [
                    language for language, _ in translated_blocks
                ]:
                    errors.append(f"{page.path}: translated fenced code languages changed")
                elif any(
                    language.lower() != "mermaid"
                    and _normalize_code_whitespace(source_body)
                    != _normalize_code_whitespace(translated_body)
                    for (language, source_body), (_, translated_body) in zip(
                        source_blocks, translated_blocks
                    )
                ):
                    errors.append(f"{page.path}: executable or example code changed")
            if translation["stale"]:
                warnings.append(f"{page.path}: Korean translation requires source review")

    for translation_path in TRANSLATION_ROOT.rglob("*.mdx"):
        resolved = translation_path.resolve()
        if resolved in known_translation_paths:
            continue
        relative = canonical_path(str(translation_path.relative_to(TRANSLATION_ROOT)))
        errors.append(f"{relative}: translation is not a canonical manifest page")

    return ValidationReport(
        pages=len(repository.pages),
        summaries=summaries,
        translations=translations,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )
