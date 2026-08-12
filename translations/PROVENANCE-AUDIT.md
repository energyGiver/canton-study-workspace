# Korean Translation Provenance Audit

## Decision

Korean documentation must be translated directly with Codex. External translation APIs, browser translation services, and separately installed local translation models are prohibited. Any page proven to have been produced by one of those systems must be removed from coverage and returned to the todo list until Codex translates it again from the official English source.

## Audit method

The 2026-08-12 audit searched all local Codex session JSONL records under `~/.codex/sessions` for the following execution evidence:

- Google Translate endpoints containing `translate.google`
- MyMemory endpoint calls containing `api.mymemory`
- Bing Translator endpoints containing `ttranslatev3` or `bing.com/translator`
- Argos Translate installation and execution containing `argostranslate` or `argosmodel`
- canonical writes under `translations/ko`
- temporary staging paths and atomic moves into the canonical translation tree

Endpoint calls were correlated with later file-write tool calls. A page was classified as affected only when the session record showed that translated output reached its canonical path. Probe requests and failed atomic batches that produced no canonical file were recorded but did not invalidate unrelated pages.

## Confirmed affected pages

| Translation mechanism | Canonical path | Audit result | Disposition |
|---|---|---|---|
| Bing Translator API | `appdev/reference/daml-lf-reference` | The API runner wrote this canonical page | Removed, returned to todo, then translated directly with Codex and restored |
| Argos local model | `appdev/app-rewards` | Local-model staging informed the canonical draft | Removed, returned to todo, then translated directly with Codex and restored |
| Argos local model | `appdev/get-started/choose-your-path` | Local-model staging informed the canonical draft | Removed, returned to todo, then translated directly with Codex and restored |
| Argos local model | `appdev/get-started/whats-new` | Local-model staging informed the canonical draft | Removed, returned to todo, then translated directly with Codex and restored |
| Argos local model | `appdev/quickstart/index` | Local-model staging informed the canonical draft | Removed, returned to todo, then translated directly with Codex and restored |

## Calls that did not produce canonical pages

- A Google Translate Global Synchronizer batch was designed to stage all output before an atomic write. It failed before creating any canonical translation file.
- Google Translate and MyMemory single-sentence requests were capability probes and did not write documentation pages.
- The macOS on-device Translation framework probe did not produce a translated page.

## Cleanup

The Argos virtual environment, downloaded language model, model cache, staging directories, and Translation framework compilation cache were moved to the user's Trash. They can be recovered from Trash until it is emptied. The external API runner and its response cache were deleted from the ignored `.generated` directory.

## Required conditions

- Update this audit if any new non-Codex translation mechanism is discovered.
- Affected pages must not count toward coverage until a direct Codex translation passes `python3 -m portal validate`.
- Keep `translations/STATUS.md` synchronized with the live canonical count.
- Do not infer provenance from writing style alone. Require session, process, staging, or file-write evidence.
