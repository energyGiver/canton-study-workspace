# Korean Translation Status

## Decision

Korean navigation exposes only complete pages that pass source traceability, structural preservation, code preservation, and MDX validation. Every current translation is an `ai_draft` and still requires human review before approval.

## Checkpoint

Snapshot date: 2026-08-12

| Documentation area | Translated | Local exclusion | Official pages | Backlog |
|---|---:|---:|---:|---:|
| Root API Reference | 1 | 0 | 1 | 0 |
| Overview | 47 | 0 | 47 | 0 |
| App Development | 143 | 2 | 145 | 0 |
| Global Synchronizer | 100 | 5 | 105 | 0 |
| Integrations | 140 | 2 | 142 | 0 |
| SDKs and Tools | 62 | 99 | 161 | 0 |
| Reference corpus | 365 | 190 | 555 | 0 |
| Release Notes | 1 | 0 | 1 | 0 |
| Shared | 3 | 0 | 3 | 0 |
| **Total** | **862** | **298** | **1,160** | **0** |

Run `python3 -m portal translations` for the live inventory and todo list, and run `python3 -m portal validate` for source/MDX integrity. Update this checkpoint in the same commit as each translation batch.

## Remaining todo

There is no current translation backlog. All 1,160 official file-backed navigation pages are either complete Korean translations or exact-path local exclusions.

The 298 exclusions are stored in the Git-ignored `data/local/translation-exclusions.json`, including a reason and category. They remain available in English, are disclosed by `python3 -m portal translations`, and are ignored during upstream translation checks only while their exact official paths remain listed. New upstream paths always enter the review backlog.

Five pages were deliberately withdrawn on 2026-08-12 because one had used an external translation API and four had used a locally installed translation model. All five were subsequently translated directly with Codex and restored.

## Required conditions

- Preserve Canton component, protocol, API, product, and application-model terminology in English.
- Translate a page completely before adding it to `translations/ko`.
- Preserve source URLs, source IDs, source hashes, headings, links, MDX structure, and executable code.
- Treat every draft as unofficial until a named human reviewer changes `translation_status` to `approved`.
- Re-review a translation whenever its recorded source hash no longer matches the official source.
