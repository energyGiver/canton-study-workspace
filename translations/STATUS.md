# Korean Translation Status

## Decision

Korean navigation exposes only complete pages that pass source traceability, structural preservation, code preservation, and MDX validation. Every current translation is an `ai_draft` and still requires human review before approval.

## Checkpoint

Snapshot date: 2026-08-12

| Documentation area | Translated | Canonical pages | Coverage |
|---|---:|---:|---:|
| Root API Reference | 1 | 1 | 100.0% |
| Overview | 47 | 47 | 100.0% |
| App Development | 142 | 145 | 97.9% |
| Global Synchronizer | 101 | 106 | 95.3% |
| Integrations | 140 | 140 | 100.0% |
| Reference corpus | 365 | 365 | 100.0% |
| **Total** | **796** | **804** | **99.0%** |

Run `python3 -m portal validate` to obtain the live totals. Update this checkpoint in the same commit as each translation batch.

## Remaining todo

- App Development: 3 pages
- Global Synchronizer: 5 pages
- Overview: 0 pages
- Total: 8 pages

Five pages were deliberately withdrawn on 2026-08-12: one page created through an external translation API and four pages derived from a locally installed translation model. All five have since been translated directly with Codex and restored.

## Required conditions

- Preserve Canton component, protocol, API, product, and application-model terminology in English.
- Translate a page completely before adding it to `translations/ko`.
- Preserve source URLs, source IDs, source hashes, headings, links, MDX structure, and executable code.
- Treat every draft as unofficial until a named human reviewer changes `translation_status` to `approved`.
- Re-review a translation whenever its recorded source hash no longer matches the official source.
