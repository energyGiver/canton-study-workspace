# Canton Documentation Research Instructions

## Writing style

- Do not use the U+00B7 Korean middle dot separator in reports, HTML, Markdown, tables, UI copy, or summaries.
- Use `/`, `&`, commas, or natural sentence phrasing instead.
- Before delivery, check generated artifacts for U+00B7 and remove it if present.
- Keep introductions and conclusions explicit: state the decision, the reason, and the required conditions.

## Evidence and research rules

1. Use official Canton documentation as the primary evidence source.
2. Do not use model memory to fill missing technical details.
3. Every important technical statement must include a source reference.
4. Clearly distinguish `EXPLICIT`, `INFERRED`, and `UNCLEAR`.
5. Prefer cross-document mechanism analysis over isolated page summaries.
6. Preserve terminology used by Canton documentation.
7. Identify contradictions or ambiguous terminology instead of silently reconciling them.
8. Record unanswered implementation questions for the later engineering phase.
9. Do not inspect Canton source code or run experiments during this phase.
10. Optimize for deep technical understanding, not brevity.

## Scope boundary

- This phase is documentation-only.
- Do not analyze Canton source repositories, execute Canton tests, deploy LocalNet or nodes, run protocol experiments, or claim implementation verification.
- Documentation about deployment, testing, and implementation may be analyzed as documentation, but its procedures must not be executed.

## Traceability convention

- Cite research statements with a stable source ID from `corpus/manifest.jsonl`, the official document title, and the relevant heading.
- Use `EXPLICIT` only for statements directly supported by the cited text.
- Use `INFERRED` only when the reasoning and all supporting sources are identified.
- Use `UNCLEAR` when the official corpus is incomplete, internally inconsistent, or insufficiently precise.
- Add unresolved gaps to `questions/open-questions.md`; do not silently resolve them.
