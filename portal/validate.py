from __future__ import annotations

from dataclasses import dataclass

from .content import ContentRepository


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
    errors: list[str] = []
    warnings: list[str] = []
    summaries = 0
    translations = 0

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
            if translation["stale"]:
                warnings.append(f"{page.path}: Korean translation requires source review")

    return ValidationReport(
        pages=len(repository.pages),
        summaries=summaries,
        translations=translations,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )
