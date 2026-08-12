# Korean Translation Status

## Decision

Korean navigation exposes only complete pages that pass source traceability, structural preservation, code preservation, and MDX validation. Every current translation is an `ai_draft` and still requires human review before approval.

## Checkpoint

Snapshot date: 2026-08-12

| Documentation area | Translated | Canonical pages | Coverage |
|---|---:|---:|---:|
| Root API Reference | 1 | 1 | 100.0% |
| Overview | 36 | 47 | 76.6% |
| App Development | 23 | 145 | 15.9% |
| Global Synchronizer | 21 | 106 | 19.8% |
| Integrations | 26 | 140 | 18.6% |
| Reference corpus | 0 | 365 | 0.0% |
| **Total** | **107** | **804** | **13.3%** |

Run `python3 -m portal validate` to obtain the live totals. Update this checkpoint in the same commit as each translation batch.

## Required conditions

- Preserve Canton component, protocol, API, product, and application-model terminology in English.
- Translate a page completely before adding it to `translations/ko`.
- Preserve source URLs, source IDs, source hashes, headings, links, MDX structure, and executable code.
- Treat every draft as unofficial until a named human reviewer changes `translation_status` to `approved`.
- Re-review a translation whenever its recorded source hash no longer matches the official source.
