# Korean Translation Status

## Decision

Korean navigation exposes only complete pages that pass source traceability, structural preservation, code preservation, and MDX validation. Every current translation is an `ai_draft` and still requires human review before approval.

## Checkpoint

Snapshot date: 2026-08-12

| Documentation area | Translated | Canonical pages | Coverage |
|---|---:|---:|---:|
| Root API Reference | 1 | 1 | 100.0% |
| Overview | 46 | 47 | 97.9% |
| App Development | 51 | 145 | 35.2% |
| Global Synchronizer | 52 | 106 | 49.1% |
| Integrations | 140 | 140 | 100.0% |
| Reference corpus | 0 | 365 | 0.0% |
| **Total** | **290** | **804** | **36.1%** |

Run `python3 -m portal validate` to obtain the live totals. Update this checkpoint in the same commit as each translation batch.

## Required conditions

- Preserve Canton component, protocol, API, product, and application-model terminology in English.
- Translate a page completely before adding it to `translations/ko`.
- Preserve source URLs, source IDs, source hashes, headings, links, MDX structure, and executable code.
- Treat every draft as unofficial until a named human reviewer changes `translation_status` to `approved`.
- Re-review a translation whenever its recorded source hash no longer matches the official source.
