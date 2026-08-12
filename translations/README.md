# Korean Translation Workflow

## Decision

Translate only the 804 canonical pages registered in `corpus/manifest.jsonl`. The official English MDX remains unchanged in `upstream/cf-docs`, while each complete Korean page is stored at the matching path under `translations/ko` and rendered as an unofficial `ai_draft` until human review.

This boundary avoids translating internal snippets, duplicated generated inputs, and files that are not independently traceable through the deployed documentation manifest.

## Language policy

1. Preserve Canton component names, protocol concepts, product names, API names, Daml terms, configuration keys, identifiers, code, and commands in English.
2. Keep frequently referenced technical nouns in English when translating them would make official documentation search or team communication harder.
3. Translate explanatory prose, connective language, examples, cautions, and user instructions into natural Korean.
4. Preserve the exact strength of authorization, privacy, trust, security, failure, and operational statements.
5. Do not add explanations, guarantees, or implementation claims that are absent from the official page.
6. Follow [the shared translation glossary](glossary.md) and extend it through review when a repeated term needs a stable decision.
7. Use Codex directly for translation. Do not use external translation APIs, browser translation services, or separately installed local translation models.

See [the translation provenance audit](PROVENANCE-AUDIT.md) for the detection criteria and the pages that were withdrawn and translated again.

## Required page format

Each Korean MDX page must retain the official frontmatter fields and add:

```yaml
source_id: "SRC-..."
source_path: "overview/understand/example"
source_commit: "<pinned cf-docs commit>"
source_sha256: "<SHA-256 of the official English MDX>"
translation_status: "ai_draft"
translated_at: "YYYY-MM-DD"
reviewed_by: null
```

Immediately after frontmatter, add a `Warning` stating that the page is an unofficial Korean translation and linking to the exact official English page. Translate the complete page before creating the file. Partial translations must not be published to `translations/ko`.

## Content preservation

- Preserve imports, exports, MDX components, JSX properties, code fences, inline code, links, anchors, images, Mermaid syntax, tables, and heading levels.
- Translate visible labels inside diagrams only when doing so does not change an identifier or syntax token.
- Do not translate filenames, package names, CLI flags, environment variables, API paths, field names, JSON keys, log fragments, or configuration examples.
- Keep source URLs and cross-document routes stable. Korean routing is added by the portal and must not be hard-coded into official cross-links.
- Do not use the U+00B7 Korean middle dot separator.

## Batch workflow

1. Select a disjoint set of canonical paths from `corpus/manifest.jsonl`.
2. Translate each page from `upstream/cf-docs/docs-main/<source_path>.mdx`.
3. For a canonical page absent from the authoring repository, use its deployed snapshot in `corpus/docs` and record that exception during review.
4. Run `python3 -m portal validate` and scan the batch for U+00B7.
5. Build the portal and review ENG/KOR rendering, code blocks, tables, callouts, links, and navigation.
6. Commit only complete pages with the configured human Git identity.

## Review states

- `ai_draft`: complete machine-assisted translation awaiting human review.
- `human_edited`: a team member has reviewed or edited the page.
- `approved`: the team accepts the translation for the recorded source hash.
- `stale`: computed by the portal when the official source hash changes and never written manually.

Translation completeness and technical correctness are separate checks. A page can be a complete `ai_draft` while still requiring technical review before it becomes `approved`.
